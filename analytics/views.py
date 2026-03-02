from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Q, F, Subquery, OuterRef
from core.models import Student, Grade, Subject
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth


@login_required
def statistics_view(request):

    selected_class = request.GET.get('class', '')

    total_students = Student.objects.count()
    total_grades = Grade.objects.count()

    avg_grade_result = Grade.objects.aggregate(avg=Avg('score'))
    avg_grade = round(avg_grade_result['avg'], 1) if avg_grade_result['avg'] else 0

    students_with_2 = Student.objects.filter(grade__score=2).distinct()
    needs_attention = students_with_2.count()

    unique_groups = Student.objects.values('group').annotate(
        student_count=Count('id')
    ).order_by('group')

    classes_list = []
    for group_data in unique_groups:
        group_name = group_data['group']
        student_count = group_data['student_count']

        student_ids = Student.objects.filter(group=group_name).values_list('id', flat=True)
        avg_grade_group = Grade.objects.filter(
            student_id__in=student_ids
        ).aggregate(avg=Avg('score'))

        avg_grade_value = round(avg_grade_group['avg'], 1) if avg_grade_group['avg'] else 0

        classes_list.append({
            'name': group_name,
            'student_count': student_count,
            'avg_grade': avg_grade_value,
            'selected': group_name == selected_class,
        })

    class_stats = None
    students_stats = []

    if selected_class:

        students_in_class = Student.objects.filter(group=selected_class).order_by('full_name')

        for student in students_in_class:

            student_grades = Grade.objects.filter(student=student).order_by('-date')
            total_student_grades = student_grades.count()

            avg_student = student_grades.aggregate(avg=Avg('score'))
            avg_grade_student = round(avg_student['avg'], 1) if avg_student['avg'] else 0

            improvement = calculate_student_dynamics(student_grades)

            recent_grades = student_grades[:5]

            students_stats.append({
                'student': student,
                'total_grades': total_student_grades,
                'avg_grade': avg_grade_student,
                'improvement': improvement,
                'recent_grades': recent_grades,
                'has_low_grades': student_grades.filter(score=2).exists(),
            })

        student_ids = students_in_class.values_list('id', flat=True)
        class_grades = Grade.objects.filter(student_id__in=student_ids)

        class_total_grades = class_grades.count()
        class_avg_grade = class_grades.aggregate(avg=Avg('score'))
        class_avg = round(class_avg_grade['avg'], 1) if class_avg_grade['avg'] else 0

        class_stats = {
            'name': selected_class,
            'student_count': students_in_class.count(),
            'total_grades': class_total_grades,
            'avg_grade': class_avg,
            'students_stats': students_stats,
        }

    top_subjects = Subject.objects.annotate(
        grade_count=Count('grade'),
        avg_grade=Avg('grade__score')
    ).filter(grade_count__gt=0).order_by('-grade_count')[:5]

    top_subjects_list = []
    for subject in top_subjects:
        top_subjects_list.append({
            'name': subject.name,
            'count': subject.grade_count,
            'avg_grade': round(subject.avg_grade, 1) if subject.avg_grade else 0
        })

    dates = []
    grades_per_day = []
    avg_grades_per_day = []

    today = timezone.now().date()
    total_grades_last_10_days = 0

    for i in range(10):
        day = today - timedelta(days=9 - i)
        dates.append(day.strftime('%d.%m'))


        grades_today = Grade.objects.filter(date=day)
        count_today = grades_today.count()
        total_grades_last_10_days += count_today

        avg_today = grades_today.aggregate(avg=Avg('score'))
        avg_value = round(avg_today['avg'], 1) if avg_today['avg'] else 0

        grades_per_day.append(count_today)
        avg_grades_per_day.append(avg_value)

    context = {
        'metrics': {
            'total_students': total_students,
            'total_grades': total_grades,
            'avg_grade': avg_grade,
            'needs_attention': needs_attention,
        },
        'classes_list': classes_list,
        'selected_class': selected_class,
        'class_stats': class_stats,
        'top_subjects': top_subjects_list,
        'dates': dates,
        'grades_per_day': grades_per_day,
        'avg_grades_per_day': avg_grades_per_day,
        'total_grades_last_10_days': total_grades_last_10_days,
    }

    return render(request, 'statistics.html', context)


def calculate_student_dynamics(grades_queryset):

    grades = list(grades_queryset)

    if len(grades) == 0:
        return "Нет оценок"

    recent_grades = grades[:3]

    has_twos = any(g.score == 2 for g in recent_grades)

    if len(recent_grades) > 0:
        recent_avg = sum(g.score for g in recent_grades) / len(recent_grades)
    else:
        recent_avg = 0

    if has_twos:
        return "⚠️ Есть 2"
    elif recent_avg >= 4.0:
        return "✓ Отлично"
    elif recent_avg >= 3.0:
        return "→ Хорошо"
    elif recent_avg >= 2.0:
        return "↘ Удовл."
    else:
        return "⚠️ Низкий"