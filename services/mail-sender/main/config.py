from pydantic import EmailStr
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # Flask Configuration
    ENV: str = 'development'
    DEBUG: int = 1

    # Message Queue Broker
    MQ_BROKER: Literal['rabbitmq', 'sqs'] = 'rabbitmq'

    # RabbitMQ
    RABBITMQ_HOST: str = 'localhost'
    RABBITMQ_PORT: int =  5672
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_QUEUE: str = 'messages'

    # SQS Configuration
    SQS_QUEUE_URL: str

    # SMTP
    SMTP_SERVER: str = 'smtp.gmail.com'
    SMTP_PORT: int = 587
    SMTP_USE_TLS: bool = True
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    EMAIL_FROM: EmailStr
    EMAIL_TO: EmailStr

    class Config:
        env_file = '.env'