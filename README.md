# Remember Everything

Remember everything you would need

## Project Overview

This project consists of multiple microservices designed to handle messaging and communication functionality.

## Services
You need to create .env file (from .env.example) and have PostgreSQL, MongoDB, Redis and RabitMQ to run it locally.

### 1. Message Receiver

A web application that provides the core messaging and user management functionality.

Location: `services/message-receiver/`

#### Get started
```
pip install -r ./requirements.txt
pip install -e ../common
```

#### Migrate DBs locally
```
python manage.py migrate
python manage.py migrate --database analytics
```

#### Run
```
celery -A main worker --loglevel=INFO --pool=eventlet
python manage.py runserver
```

#### Deploy
```
./deploy.sh
```

### 2. Mail Sender

A dedicated service for handling email sending.

Location: `services/mail-sender/`

#### Get started
```
pip install -r ./requirements.txt
pip install -e ../common
python run.py
```

#### Deploy
```
./deploy.sh
```

### 3. Ticket Booking API

A REST API for booking train tickets.

#### Get started

```
pip install -r ./requirements.txt
uvicorn main:app --reload
```
