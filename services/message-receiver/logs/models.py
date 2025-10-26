from mongoengine import Document, StringField, DateTimeField
from datetime import datetime, timezone


class UserInteractionLog(Document):
    user_login = StringField(required=True, max_length=150)
    action = StringField(required=True, max_length=50)
    details = StringField(max_length=500)
    timestamp = DateTimeField(default=lambda: datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0))
    ip_address = StringField(max_length=45)
    user_agent = StringField(max_length=500)
    
    meta = {
        'collection': 'user_interaction_logs',
        'indexes': [
            'user_login',
            'action',
            '-timestamp',
            ('user_login', '-timestamp'),
        ],
        'ordering': ['-timestamp']
    }
    
    def __str__(self):
        return f"{self.user_login} - {self.action} at {self.timestamp}"
