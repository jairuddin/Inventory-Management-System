from rest_framework import serializers
from .models import InventronItem

class InventronItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventronItem
        fields = ['id', 'item_name', 'item_description', 'item_quantity', 'created_at']
