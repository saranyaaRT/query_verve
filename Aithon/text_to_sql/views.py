from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .models import InteractionModel, MessageModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import InteractionSerializer, MessageSerializer
from .language_model import generate_chat_response
from .trino_md import get_image_data
import pandas as pd


@api_view(["GET"])
def get_messages_by_thread(request, thread_id):
    """Fetch all messages related to a given thread_id"""
    messages = MessageModel.objects.all().order_by("timestamp")
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_or_update_interaction(request):

    thread_id = request.data.get("thread_id")
    prompt_text = request.data.get("query_text")

    if not thread_id:
        return Response({"error": "thread_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    session_id = "viewbnuqlkn"
    interaction = InteractionModel.objects.create(session_id=session_id, thread_id=thread_id)
    MessageModel.objects.create(interaction=interaction, text=prompt_text, type="user")
    result = generate_chat_response(prompt_text)
    # print(result)
    df = get_image_data(result)
    response = df.loc[:20].to_markdown()
    message = MessageModel.objects.create(interaction=interaction, text=response, type="ai")

    interaction_serializer = InteractionSerializer(interaction)
    message_serializer = MessageSerializer(message)

    return Response(
        {
            "message": message_serializer.data
        },
        status=status.HTTP_201_CREATED
    )



