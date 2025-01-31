from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .models import InteractionModel, MessageModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import InteractionSerializer, MessageSerializer
from .language_model import call_gpt , create_session


@api_view(["GET"])
def get_messages_by_thread(request, thread_id):
    """Fetch all messages related to a given thread_id"""
    interaction = get_object_or_404(InteractionModel, thread_id=thread_id)
    messages = interaction.messages.all().order_by("timestamp")
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_or_update_interaction(request):

    thread_id = request.data.get("thread_id")
    prompt_text = request.data.get("query_text")

    if not thread_id:
        return Response({"error": "thread_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if interaction exists
    interaction = InteractionModel.objects.filter(thread_id=thread_id).first()

    if interaction:
        session_id = interaction.session_id
    else:

        session_id = create_session()
        interaction = InteractionModel.objects.create(session_id=session_id, thread_id=thread_id)
    MessageModel.objects.create(interaction=interaction, text=prompt_text, type="user")
    result = call_gpt(session_id)
    message = MessageModel.objects.create(interaction=interaction, text=result, type="ai")

    interaction_serializer = InteractionSerializer(interaction)
    message_serializer = MessageSerializer(message)

    return Response(
        {
            "interaction": interaction_serializer.data,
            "message": message_serializer.data
        },
        status=status.HTTP_201_CREATED
    )



