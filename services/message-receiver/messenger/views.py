from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm
from .rabbitmq import send_to_rabbitmq


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            success = send_to_rabbitmq(message.content)

            if success:
                message.sent_to_rabbitmq = True
                message.save()
                messages.success(request, 'Message sent successfully!')
                return redirect('send_message')
            else:
                messages.error(request, 'Failed to send message to RabbitMQ. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MessageForm()

    return render(request, 'messenger/send_message.html', {'form': form})