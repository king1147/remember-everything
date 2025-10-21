import os
import sys

# Add a project to a path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

import django
django.setup()

import awsgi
from main.wsgi import application


def handler(event, context):
    """
    AWS Lambda handler function for WSGI
    """
    return awsgi.response(application, event, context)
