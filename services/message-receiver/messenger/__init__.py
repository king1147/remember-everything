from common.message_queue import MessageQueue
from django.conf import settings

config = {
    'MQ_BROKER': settings.MQ_BROKER,
    'RABBITMQ_HOST': settings.RABBITMQ_HOST,
    'RABBITMQ_PORT': settings.RABBITMQ_PORT,
    'RABBITMQ_USER': settings.RABBITMQ_USER,
    'RABBITMQ_PASSWORD': settings.RABBITMQ_PASSWORD,
    'RABBITMQ_EXCHANGE': settings.RABBITMQ_EXCHANGE,
    'RABBITMQ_ROUTING_KEY': settings.RABBITMQ_ROUTING_KEY,
    'SQS_QUEUE_URL': settings.SQS_QUEUE_URL
}

mq = MessageQueue(config)