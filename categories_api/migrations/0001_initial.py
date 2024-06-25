# Generated by Django 5.0.6 on 2024-06-25 12:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('label', models.CharField(choices=[('Work', 'Work'), ('Family', 'Family'), ('Relatives', 'Relatives'), ('University', 'University')], max_length=50, unique=True)),
            ],
        ),
    ]
