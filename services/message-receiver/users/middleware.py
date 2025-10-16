from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    allowed_paths = [
        reverse('login'),
        reverse('register'),
    ]
    allowed_prefixes = ['/static/', '/admin/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'user_id' not in request.session:
            if (request.path not in self.allowed_paths
                    and not any(request.path.startswith(prefix) for prefix in self.allowed_prefixes)):
                return redirect('login')

        return self.get_response(request)