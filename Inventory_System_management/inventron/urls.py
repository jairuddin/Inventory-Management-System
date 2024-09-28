from django.urls import path
from .views import (InventronItemListCreateAPIView,InventronItemDetailAPIView)

urlpatterns = [
    path('items/', InventronItemListCreateAPIView.as_view(), name='item-list-create'),  # List all items or create a new item
    path('items/<int:pk>/', InventronItemDetailAPIView.as_view(), name='item-detail'),  # Get, update, or delete an item by ID
]
