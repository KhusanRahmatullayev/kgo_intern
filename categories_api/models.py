from django.db import models

from django.db import models
import uuid

class Category(models.Model):
    class CategoryChoices(models.TextChoices):
        WORK = 'Work', 'Work'
        FAMILY = 'Family', 'Family'
        RELATIVES = 'Relatives', 'Relatives'
        UNIVERSITY = 'University', 'University'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        unique=True,
    )

    def __str__(self):
        return self.label

