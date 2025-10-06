import pika
import logging
import time
from .email_sender import EmailSender

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    def __init__(self, config):
        self.config = config
        self.email_sender = EmailSender(config)
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(
                self.config['RABBITMQ_USER'],
                self.config['RABBITMQ_PASSWORD']
            )

            parameters = pika.ConnectionParameters(
                host=self.config['RABBITMQ_HOST'],
                port=self.config['RABBITMQ_PORT'],
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            self.channel.basic_qos(prefetch_count=1)

            logger.info(f"Connected to RabbitMQ at {self.config['RABBITMQ_HOST']}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            return False

    def callback(self, ch, method, properties, body):
        """Process received message"""
        try:
            message = body.decode('utf-8')
            logger.info(f"Received message: {message}")

            # Send email
            if self.email_sender.send_email(message):
                ch.basic_ack(delivery_tag=method.delivery_tag)
                logger.info("Message processed successfully")
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                logger.warning("Message requeued due to email failure")

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start_consuming(self):
        """Start consuming messages from RabbitMQ"""
        while True:
            try:
                if not self.connection or self.connection.is_closed:
                    if not self.connect():
                        logger.error("Failed to connect. Retrying in 5 seconds...")
                        time.sleep(5)
                        continue

                logger.info(f"Waiting for messages from queue: {self.config['RABBITMQ_QUEUE']}")
                logger.info("Press CTRL+C to exit")

                self.channel.basic_consume(
                    queue=self.config['RABBITMQ_QUEUE'],
                    on_message_callback=self.callback,
                    auto_ack=False
                )

                self.channel.start_consuming()

            except KeyboardInterrupt:
                logger.info("Stopping consumer...")
                if self.channel:
                    self.channel.stop_consuming()
                if self.connection:
                    self.connection.close()
                break

            except Exception as e:
                logger.error(f"Consumer error: {str(e)}")
                logger.info("Reconnecting in 5 seconds...")
                time.sleep(5)