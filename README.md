# Remember Everything

Remember everything you would need

## Project Overview

This project consists of multiple microservices designed to handle messaging and communication functionality.

## Services

### 1. Message Receiver

A web application that provides the core messaging and user management functionality.

Location: `services/message-receiver/`

#### Get started
You need to have PostgreSQL and RabitMQ installed locally.
```
pip install -r .\requirements.txt
python manage.py runserver
```

#### Migrate DBs locally
```
python manage.py migrate
python manage.py migrate --database analytics
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
pip install -r .\requirements.txt
python run.py
```

#### Deploy
```
./deploy.sh
```
