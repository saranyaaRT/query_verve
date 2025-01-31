
from django.db import models

class InteractionModel(models.Model):
    session_id = models.CharField(max_length=255)
    thread_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Interaction {self.thread_id}"

class MessageModel(models.Model):
    interaction = models.ForeignKey(InteractionModel, on_delete=models.CASCADE, related_name="messages")
    # user = models.CharField(max_length=255)  # Store user identifier (e.g., username, ID)
    text = models.TextField()
    type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set timestamp

    def __str__(self):
        return f"Message by {self.user}: {self.text[:50]}"

