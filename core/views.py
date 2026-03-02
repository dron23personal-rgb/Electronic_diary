from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):

    return render(request, 'home.html')


@login_required
def statistics_view(request):

    import random
    from datetime import datetime, timedelta

    days = 30
    dates = [(datetime.now() - timedelta(days=i)).strftime('%d.%m') for i in range(days)]
    dates.reverse()

    classes_stats = [
        {'name': '10А', 'students': 25, 'avg_grade': 4.2, 'improvement': '+5%'},
        {'name': '10Б', 'students': 22, 'avg_grade': 3.8, 'improvement': '+2%'},
        {'name': '11А', 'students': 28, 'avg_grade': 4.5, 'improvement': '+8%'},
        {'name': '11Б', 'students': 24, 'avg_grade': 3.9, 'improvement': '-1%'},
    ]

    top_subjects = [
        {'name': 'Математика', 'avg_grade': 4.5, 'count': 150},
        {'name': 'Физика', 'avg_grade': 4.2, 'count': 120},
        {'name': 'Русский язык', 'avg_grade': 4.0, 'count': 130},
        {'name': 'История', 'avg_grade': 4.3, 'count': 90},
        {'name': 'Химия', 'avg_grade': 3.8, 'count': 80},
    ]

    metrics = {
        'total_students': 99,
        'total_grades': 1248,
        'avg_grade': 4.2,
        'needs_attention': 12,
    }

    context = {
        'dates': dates[:10],
        'classes_stats': classes_stats,
        'top_subjects': top_subjects,
        'metrics': metrics,
    }

    return render(request, 'statistics.html', context)