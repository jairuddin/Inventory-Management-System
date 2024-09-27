
from django.core.cache import cache  
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InventronItem
from .serializers import InventronItemSerializer
import json

class InventronItemListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # JWT token required for access

    def get(self, request):
        # Get all items
        items = InventronItem.objects.all()
        serializer = InventronItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new item
        serializer = InventronItemSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the item already exists
            if InventronItem.objects.filter(item_name=request.data['item_name']).exists():
                return Response({"detail": "Item already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventronItemDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  # JWT token required for access

    def get_object(self, pk):
        # Check the Redis cache for the item
        cache_key = f'inventron_item_{pk}'
        cached_item = cache.get(cache_key)

        if cached_item:
            # If item found in cache, return it
            return json.loads(cached_item)

        # If not found in cache, fetch from database
        try:
            return InventronItem.objects.get(pk=pk)
        except InventronItem.DoesNotExist:
            return None

    def get(self, request, pk):
        # Read item by ID
        item = self.get_object(pk)
        if item is None:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the item
        serializer = InventronItemSerializer(item)
        
        # Store the item in Redis cache for subsequent requests
        cache_key = f'inventron_item_{pk}'
        cache.set(cache_key, json.dumps(serializer.data), timeout=60*15)  # Cache for 15 minutes
        
        return Response(serializer.data)

    def put(self, request, pk):
        # Update item by ID
        item = self.get_object(pk)
        if item is None:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InventronItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Invalidate cache since item is updated
            cache.delete(f'inventron_item_{pk}')
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete item by ID
        item = self.get_object(pk)
        if item is None:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        # Invalidate cache since item is deleted
        cache.delete(f'inventron_item_{pk}')
        return Response({"message": "Item deleted"}, status=status.HTTP_204_NO_CONTENT)
