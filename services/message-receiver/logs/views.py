from django.shortcuts import render
from django.core.paginator import Paginator
from .models import UserInteractionLog
from .forms import LogFilterForm


def log_viewer(request):
    """View to display and filter user interaction logs"""
    form = LogFilterForm(request.GET or None)

    logs_query = UserInteractionLog.objects.all()

    if form.is_valid():
        user_login = form.cleaned_data.get('user_login')
        action = form.cleaned_data.get('action')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        if user_login:
            logs_query = logs_query.filter(user_login__icontains=user_login)
        
        if action:
            logs_query = logs_query.filter(action=action)
        
        if start_date:
            logs_query = logs_query.filter(timestamp__gte=start_date)
        
        if end_date:
            logs_query = logs_query.filter(timestamp__lte=end_date)

    logs_query = logs_query.order_by('-timestamp')

    paginator = Paginator(list(logs_query), 20)  # Show 20 logs per page
    page_number = request.GET.get('page', 1)
    logs = paginator.get_page(page_number)

    total_logs = logs_query.count()
    unique_users = len(logs_query.distinct('user_login'))
    
    context = {
        'form': form,
        'logs': logs,
        'total_logs': total_logs,
        'unique_users': unique_users,
    }
    
    return render(request, 'logs/log_viewer.html', context)
