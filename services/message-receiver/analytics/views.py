from django.shortcuts import render
from django.db.models import Count, Avg, Q
from .models import MessageAnalytics


def analytics_dashboard(request):
    stats = MessageAnalytics.objects.using('analytics').aggregate(
        total_messages=Count('id'),
        avg_processing_time=Avg('processing_time_ms'),
        successful_sends=Count('id', filter=Q(sent_to_rabbitmq=True))
    )

    recent = MessageAnalytics.objects.using('analytics').order_by('-created_at')[:10]

    return render(request, 'analytics/dashboard.html', {
        'stats': stats,
        'recent': recent
    })