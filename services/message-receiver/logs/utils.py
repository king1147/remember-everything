from .models import UserInteractionLog


def log_user_action(user_login, action, details='', request=None):
    """
    Log user interactions
    """
    log_data = {
        'user_login': user_login,
        'action': action,
        'details': details,
    }

    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        log_data['ip_address'] = ip_address
        log_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')[:500]

    try:
        log = UserInteractionLog(**log_data)
        log.save()
        return True
    except Exception as e:
        print(f"Error logging user action: {e}")
        return False