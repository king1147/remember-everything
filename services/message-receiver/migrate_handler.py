import os
import django
from django.core.management import call_command


def lambda_handler(event, context):
    """
    Lambda handler for running Django migrations
    """
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
        django.setup()

        # Run migrations
        print("Starting database migrations...")
        call_command('migrate', '--noinput')
        call_command('migrate', '--noinput', database='analytics')
        print("Migrations completed successfully!")

        return {
            'statusCode': 200,
            'body': 'Migrations completed successfully'
        }

    except Exception as e:
        print(f"Migration failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Migration failed: {str(e)}'
        }