from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import InventronItem
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class InventronItemTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Generate JWT tokens for the user
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Set the authorization header for requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create a sample item for testing
        self.item_data = {
            "item_name": "Test Item",
            "item_description": "This is a test item.",
            "item_quantity": 10
        }
        self.item = InventronItem.objects.create(**self.item_data)

    def test_create_item(self):
        # Test creating a new item
        response = self.client.post(reverse('item-list-create'), {
            "item_name": "New Item",
            "item_description": "This is a new item.",
            "item_quantity": 5
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Ensure the item was created
        self.assertEqual(response.data['item_name'], "New Item")  # Check the item name

    def test_create_item_already_exists(self):
        # Test creating an item that already exists
        response = self.client.post(reverse('item-list-create'), self.item_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Ensure bad request
        self.assertEqual(response.data['detail'], "Item already exists.")  # Check error message

    def test_get_item(self):
        # Test retrieving the item by ID
        response = self.client.get(reverse('item-detail', kwargs={'pk': self.item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure the request was successful
        self.assertEqual(response.data['item_name'], self.item.item_name)  # Check the item name

    def test_get_item_not_found(self):
        # Test retrieving a non-existent item
        response = self.client.get(reverse('item-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Ensure not found response
        self.assertEqual(response.data['error'], "Item not found")  # Check error message

    def test_update_item(self):
        # Test updating an existing item
        response = self.client.put(reverse('item-detail', kwargs={'pk': self.item.id}), {
            "item_name": "Updated Item",
            "item_description": "This is an updated item.",
            "item_quantity": 20
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure the request was successful
        self.item.refresh_from_db()  # Refresh from the database to get updated values
        self.assertEqual(self.item.item_name, "Updated Item")  # Check the updated item name

    def test_update_item_not_found(self):
        # Test updating a non-existent item
        response = self.client.put(reverse('item-detail', kwargs={'pk': 999}), {
            "item_name": "Updated Item",
            "item_description": "This is an updated item.",
            "item_quantity": 20
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Ensure not found response
        self.assertEqual(response.data['error'], "Item not found")  # Check error message

    def test_delete_item(self):
        # Test deleting an existing item
        response = self.client.delete(reverse('item-detail', kwargs={'pk': self.item.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Ensure the request was successful

        # Verify the item has been deleted
        response = self.client.get(reverse('item-detail', kwargs={'pk': self.item.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Ensure item is not found

    def test_delete_item_not_found(self):
        # Test deleting a non-existent item
        response = self.client.delete(reverse('item-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Ensure not found response
        self.assertEqual(response.data['error'], "Item not found")  # Check error message
