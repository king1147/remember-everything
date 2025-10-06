import pika
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_to_rabbitmq(message_content):
    """Send message to RabbitMQ queue"""
    try:
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASSWORD
        )

        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Publish message
        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=settings.RABBITMQ_ROUTING_KEY,
            body=message_content,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        connection.close()
        logger.info(f"Message sent to RabbitMQ: {message_content[:50]}...")
        return True

    except Exception as e:
        logger.error(f"Error sending message to RabbitMQ: {str(e)}")
        return False