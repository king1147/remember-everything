from pika.exceptions import AMQPConnectionError, StreamLostError
import time
import pika
import boto3
import logging

logger = logging.getLogger(__name__)
    
class MessageQueue:
    def __init__(self, config, email_sender=None):
        self.config = config
        self.email_sender = email_sender

        if self.config['MQ_BROKER'] == 'sqs':
            self._init_sqs()
        else:
            self._init_rabbitmq()

    # RabbitMQ part
    def _init_rabbitmq(self):
        """Initialize RabbitMQ"""
        self.parameters = pika.ConnectionParameters(
            host=self.config['RABBITMQ_HOST'],
            port=self.config['RABBITMQ_PORT'],
            credentials=pika.PlainCredentials(self.config['RABBITMQ_USER'], self.config['RABBITMQ_PASSWORD']),
            heartbeat = 60,
            blocked_connection_timeout = 120
        )
        self.connection = None
        self.channel = None

        self._connect_rabbitmq()

    def _connect_rabbitmq(self):
        """Try to connect to RabbitMQ"""
        for attempt in range(5):
            try:
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                self.channel.basic_qos(prefetch_count=1)
                print('[RabbitMQ] Connected successfully.')
                return
            except AMQPConnectionError as e:
                print(f'[RabbitMQ] Connection failed (attempt {attempt + 1}/5): {e}')
                time.sleep(3)
        raise ConnectionError('[RabbitMQ] Could not connect after multiple attempts.')

    def _ensure_rabbitmq_connection(self):
        """Reconnect if the RabbitMQ connection was lost"""
        if not self.connection or self.connection.is_closed:
            print('[RabbitMQ] Connection lost. Reconnecting...')
            self._connect_rabbitmq()

    def _send_rabbitmq(self, message):
        """Send a message to RabbitMQ queue"""
        self._ensure_rabbitmq_connection()
        try:
            self.channel.basic_publish(
                exchange=self.config['RABBITMQ_EXCHANGE'],
                routing_key=self.config['RABBITMQ_ROUTING_KEY'],
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)
            )
        except (AMQPConnectionError, StreamLostError):
            print('[RabbitMQ] Connection lost during send. Reconnecting and retrying...')
            self._connect_rabbitmq()
            self._send_rabbitmq(message)

    def _callback_rabbitmq(self, ch, method, properties, body):
        """Received a message from a consumer"""
        try:
            message = body.decode('utf-8')
            logger.info(f"Received message: {message}")

            if self.email_sender.send_email(message):
                ch.basic_ack(delivery_tag=method.delivery_tag)
                logger.info("Message processed successfully")
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                logger.warning("Message processed failed")

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    #SQS part
    def _init_sqs(self):
        """Initialize SQS client"""
        if not self.config['SQS_QUEUE_URL']:
            raise ValueError('[SQS] Missing SQS_QUEUE_URL environment variable.')
        self.client = boto3.client('sqs')
        print('[SQS] Client initialized.')

    def _send_sqs(self, message):
        """Send message to SQS"""
        self.client.send_message(
            QueueUrl=self.config['SQS_QUEUE_URL'],
            MessageBody=message,
        )

    #Public methods
    def send(self, message):
        """Send a message"""
        try:
            if self.config['MQ_BROKER'] == 'sqs':
                self._send_sqs(message)
            else:
                self._send_rabbitmq(message)
            logger.info(f'Message sent: {message}')
            return True

        except Exception as e:
            logger.error(f'Error sending message: {str(e)}')
            return False

    def start_consuming(self):
        """Start consuming messages"""
        if self.config['MQ_BROKER'] == 'sqs':
            logger.error(f'Method start_consuming() not supported for {self.config["MQ_BROKER"]} broker')
            return None
        else:
            while True:
                try:
                    self._ensure_rabbitmq_connection()

                    logger.info(f'Waiting for messages from queue: {self.config['RABBITMQ_QUEUE']}')
                    logger.info('Press CTRL+C to exit')

                    self.channel.basic_consume(
                        queue=self.config['RABBITMQ_QUEUE'],
                        on_message_callback=self._callback_rabbitmq,
                        auto_ack=False
                    )

                    self.channel.start_consuming()

                except KeyboardInterrupt:
                    logger.info('Stopping consumer...')
                    self.close()
                    break

                except Exception as e:
                    logger.error(f'Consumer error: {str(e)}')
                    logger.info('Reconnecting in 10 seconds...')
                    time.sleep(10)

    def close(self):
        if self.config['MQ_BROKER'] == 'rabbitmq' and self.connection and not self.connection.is_closed:
            self.channel.stop_consuming()
            self.connection.close()
            print('Connection closed')
