from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm
from .rabbitmq import send_to_rabbitmq
from analytics.models import MessageAnalytics
from users.models import User
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
            success = send_to_rabbitmq(message.content)
            processing_time = int((time.time() - start_time) * 1000)

            if success:
                message.sent_to_rabbitmq = True
                message.save()

                MessageAnalytics.objects.using('analytics').create(
                    message_id=message.id,
                    user_login=User.objects.get(id=user_id).login,
                    content_length=len(message.content),
                    sent_to_rabbitmq=True,
                    processing_time_ms=processing_time
                )
                messages.success(request, 'Message sent successfully!')
                return redirect('send_message')
            else:
                messages.error(request, 'Failed to send message to RabbitMQ. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MessageForm()

    return render(request, 'messenger/send_message.html', {'form': form})