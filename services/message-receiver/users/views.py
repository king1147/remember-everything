from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import User
from logs.utils import log_user_action


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                log_user_action(
                    user_login=user.login,
                    action='register',
                    details='User registered successfully',
                    request=request
                )
                messages.success(request, 'Registration successful!')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    return render(request, 'users/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_username = form.cleaned_data['login']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(login=login_username)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session['user_login'] = user.login
                    
                    log_user_action(
                        user_login=user.login,
                        action='login',
                        details='User logged in successfully',
                        request=request
                    )
                    
                    messages.success(request, f'Welcome back, {user.login}!')
                    return redirect('send_message')
                else:
                    log_user_action(
                        user_login=login_username,
                        action='login_failed',
                        details='Invalid password',
                        request=request
                    )
                    messages.error(request, 'Invalid login or password.')
            except User.DoesNotExist:
                log_user_action(
                    user_login=login_username,
                    action='login_failed',
                    details='User does not exist',
                    request=request
                )
                messages.error(request, 'Invalid login or password.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout(request):
    user_login = request.session.get('user_login', 'Unknown')
    
    log_user_action(
        user_login=user_login,
        action='logout',
        details='User logged out',
        request=request
    )
    
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
