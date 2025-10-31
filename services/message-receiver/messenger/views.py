from django.shortcuts import render, redirect
from django.contrib import messages
from . import mq
from .forms import MessageForm
from analytics.models import MessageAnalytics
from users.models import User
from logs.utils import log_user_action
import time


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            user_id = request.session.get('user_id')
            if user_id:
                message.user = User.objects.get(id=user_id)

            start_time = time.time()
            success = mq.send(message.content)
            processing_time = int((time.time() - start_time) * 1000)

            if success:
                message.sent_to_mq = True
                message.save()

                user_login = User.objects.get(id=user_id).login
                
                MessageAnalytics.objects.using('analytics').create(
                    message_id=message.id,
                    user_login=user_login,
                    content_length=len(message.content),
                    sent_to_mq=True,
                    processing_time_ms=processing_time
                )

                log_user_action(
                    user_login=user_login,
                    action='send_message',
                    details=f'Message sent (length: {len(message.content)}, processing: {processing_time}ms)',
                    request=request
                )
                
                messages.success(request, 'Message sent successfully!')
                return redirect('send_message')
            else:
                log_user_action(
                    user_login=User.objects.get(id=user_id).login,
                    action='send_message_failed',
                    details='Failed to send message',
                    request=request
                )
                messages.error(request, 'Failed to send message. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MessageForm()

    return render(request, 'messenger/send_message.html', {'form': form})