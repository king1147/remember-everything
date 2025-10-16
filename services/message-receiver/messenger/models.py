from django.db import models
from users.models import User


class Message(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to_rabbitmq = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.content}"
