from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['content', 'created_at', 'sent_to_mq']
    list_filter = ['sent_to_mq', 'created_at']
    readonly_fields = ['created_at']