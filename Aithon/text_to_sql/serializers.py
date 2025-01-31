from rest_framework import serializers
from .models import InteractionModel, MessageModel

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = '__all__'

class InteractionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = InteractionModel
        fields = '__all__'
