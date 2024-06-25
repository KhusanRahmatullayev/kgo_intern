from django.db import models
import uuid

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    category = models.ForeignKey('categories_api.Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name