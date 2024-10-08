from django.db import models

class InventronItem(models.Model):
    item_name = models.CharField(max_length=100, unique=True)  
    item_description = models.TextField()  
    item_quantity = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name
