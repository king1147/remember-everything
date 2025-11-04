from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from main.settings import redis_client
from .tasks import calculate


@require_http_methods(["GET", "POST"])
def calculate_input(request):
    if request.method == "POST":
        input_expr = request.POST.get('input_expr', '')
        if input_expr:
            calculate.delay(input_expr)
        return redirect('calculate_results')

    return render(request, 'calculate/input.html')


def calculate_results(request):
    results = []
    keys = redis_client.keys('calc:*')

    for key in keys:
        result = redis_client.get(key)
        if result:
            results.append({
                'key': key,
                'value': result
            })

    context = {
        'results': results
    }
    return render(request, 'calculate/results.html', context)