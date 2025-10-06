from django.db import models


class Message(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to_rabbitmq = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.content}"
