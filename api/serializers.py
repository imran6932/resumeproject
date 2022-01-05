from django.db.models.base import Model
from rest_framework import serializers

from .models import my_input

class MyInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_input
        fields = '__all__'