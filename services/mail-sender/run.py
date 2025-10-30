from main.rabbitmq_consumer import RabbitMQConsumer
from main import create_app
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

consumer = None
consumer_thread = None

app = create_app()


def start_consumer():
    """Start RabbitMQ consumer"""
    global consumer
    consumer = RabbitMQConsumer(app.config)
    consumer.start_consuming()


if __name__ == '__main__':
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5001)