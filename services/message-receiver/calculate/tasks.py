from celery import shared_task
from main.settings import redis_client


@shared_task
def calculate(expression):
    try:
        result = eval(expression)
    except (ZeroDivisionError, TypeError) as e:
        result = f"Error: {e}"
    except SyntaxError:
        result = f"Error: Invalid syntax in expression '{expression}'"
    except Exception as e:
        result = f"Error: {e}"

    redis_client.set(f"calc:{expression}", result)
    return result