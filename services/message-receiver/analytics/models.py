from django.db import models


class MessageAnalytics(models.Model):
    message_id = models.IntegerField()
    user_login = models.CharField(max_length=150)
    content_length = models.IntegerField()
    sent_to_rabbitmq = models.BooleanField(default=False)
    processing_time_ms = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'analytics'
        db_table = 'message_analytics'
        indexes = [
            models.Index(fields=['user_login', '-created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Analytics for message {self.message_id}"


class DailyStats(models.Model):
    date = models.DateField(unique=True)
    total_messages = models.IntegerField(default=0)
    successful_sends = models.IntegerField(default=0)
    failed_sends = models.IntegerField(default=0)
    unique_users = models.IntegerField(default=0)

    class Meta:
        app_label = 'analytics'
        db_table = 'daily_stats'

    def __str__(self):
        return f"Stats for {self.date}"