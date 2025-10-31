from common.message_queue import MessageQueue
from main.email_sender import EmailSender
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

def process_message(message):
    """Process message"""
    email_sender = EmailSender(app.config)
    email_sender.send_email(message)


def start_consumer():
    """Start consumer"""
    global consumer
    consumer = MessageQueue(app.config, EmailSender(app.config))
    consumer.start_consuming()


if __name__ == '__main__':
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5001)