from rest_framework import serializers
from .models import Contact
from simple_history.utils import update_change_reason

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ContactHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact.history.model
        fields = '__all__'