from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from core.models import Student, Grade, Subject
from datetime import date, timedelta
from django.contrib import messages
from .forms import StudentForm, GradeForm
from django.core.paginator import Paginator
from .forms import GradeCreateForm

@login_required
def grade_edit(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)

    if grade.teacher != request.user:
        messages.error(request, 'Вы можете редактировать только свои оценки!')
        return redirect('teachers:student_detail', student_id=grade.student.id)

    if request.method == 'POST':
        form = GradeCreateForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оценка успешно обновлена!')
            return redirect('teachers:student_detail', student_id=grade.student.id)
    else:
        form = GradeCreateForm(instance=grade)

    context = {
        'form': form,
        'grade': grade,
        'title': f'Редактирование оценки: {grade.student.full_name}',
    }
    return render(request, 'teachers/edit_grade.html', context)


@login_required
def grade_create(request):
    if request.method == 'POST':
        form = GradeCreateForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.teacher = request.user
            grade.save()
            messages.success(request, 'Оценка успешно добавлена!')
            return redirect('teachers:student_detail', student_id=grade.student.id)
    else:
        form = GradeCreateForm()

    context = {
        'form': form,
        'title': 'Добавить оценку',
    }
    return render(request, 'teachers/add_grade.html', context)


@login_required
def teacher_dashboard(request):

    teacher_grades = Grade.objects.filter(teacher=request.user)

    recent_grades = teacher_grades.order_by('-date', '-created_at')[:10]

    students_with_2 = Student.objects.filter(
        grade__teacher=request.user,
        grade__score=2
    ).distinct()

    teacher_subjects = Subject.objects.filter(
        grade__teacher=request.user
    ).distinct().order_by('name')

    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)

    monthly_stats = teacher_grades.filter(
        date__gte=first_day_of_month
    ).aggregate(
        count=Count('id'),
        avg=Avg('score')
    )

    context = {
        'recent_grades': recent_grades,
        'students_with_2': students_with_2,
        'teacher_subjects': teacher_subjects,
        'monthly_stats': monthly_stats,
        'today': today,
    }

    return render(request, 'teachers/dashboard.html', context)


@login_required
def student_list(request):

    selected_group = request.GET.get('group', '')
    search_query = request.GET.get('search', '')

    students = Student.objects.all().order_by('group', 'full_name')

    if selected_group:
        students = students.filter(group=selected_group)

    if search_query:
        students = students.filter(
            Q(full_name__icontains=search_query) |
            Q(group__icontains=search_query)
        )

    unique_groups = Student.objects.values_list('group', flat=True).distinct().order_by('group')

    paginator = Paginator(students, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    students_with_stats = []
    for student in page_obj:
        grades = Grade.objects.filter(student=student)

        total_grades = grades.count()
        avg_grade = grades.aggregate(avg=Avg('score'))['avg']
        avg_grade = round(avg_grade, 1) if avg_grade else 0

        last_grade = grades.order_by('-date').first()

        has_twos = grades.filter(score=2).exists()

        students_with_stats.append({
            'student': student,
            'total_grades': total_grades,
            'avg_grade': avg_grade,
            'last_grade': last_grade,
            'has_twos': has_twos,
        })

    context = {
        'page_obj': page_obj,
        'students_with_stats': students_with_stats,
        'unique_groups': unique_groups,
        'selected_group': selected_group,
        'search_query': search_query,
    }

    return render(request, 'teachers/student_list.html', context)


@login_required
def student_detail(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    grades = Grade.objects.filter(student=student).order_by('-date')

    total_grades = grades.count()
    avg_grade = grades.aggregate(avg=Avg('score'))['avg']
    avg_grade = round(avg_grade, 1) if avg_grade else 0

    grades_by_subject = {}
    for grade in grades:
        subject_name = grade.subject.name
        if subject_name not in grades_by_subject:
            grades_by_subject[subject_name] = {
                'grades': [],
                'avg': 0,
                'count': 0,
            }
        grades_by_subject[subject_name]['grades'].append(grade)

    for subject_name, data in grades_by_subject.items():
        subject_grades = [g.score for g in data['grades']]
        data['avg'] = round(sum(subject_grades) / len(subject_grades), 1)
        data['count'] = len(subject_grades)

    if request.method == 'POST':
        grade_form = GradeForm(request.POST)
        if grade_form.is_valid():
            grade = grade_form.save(commit=False)
            grade.student = student
            grade.teacher = request.user
            grade.save()
            messages.success(request, 'Оценка успешно добавлена!')
            return redirect('teachers:student_detail', student_id=student.id)
    else:
        grade_form = GradeForm()

    context = {
        'student': student,
        'grades': grades,
        'total_grades': total_grades,
        'avg_grade': avg_grade,
        'grades_by_subject': grades_by_subject,
        'grade_form': grade_form,
    }

    return render(request, 'teachers/student_detail.html', context)


@login_required
def student_create(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Ученик {student.full_name} успешно создан!')
            return redirect('teachers:student_list')
    else:
        form = StudentForm()

    context = {
        'form': form,
        'title': 'Добавить ученика',
    }

    return render(request, 'teachers/student_form.html', context)


@login_required
def student_edit(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Информация об ученике {student.full_name} обновлена!')
            return redirect('teachers:student_detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'student': student,
        'title': f'Редактирование: {student.full_name}',
    }

    return render(request, 'teachers/student_form.html', context)


@login_required
def student_delete(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student_name = student.full_name
        student.delete()
        messages.success(request, f'Ученик {student_name} удален!')
        return redirect('teachers:student_list')

    context = {
        'student': student,
    }

    return render(request, 'teachers/student_delete.html', context)


@login_required
def add_grade(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student = student
            grade.teacher = request.user
            grade.save()
            messages.success(request, 'Оценка успешно добавлена!')
            return redirect('teachers:student_detail', student_id=student.id)
    else:
        form = GradeForm()

    context = {
        'form': form,
        'student': student,
        'title': f'Добавить оценку: {student.full_name}',
    }

    return render(request, 'teachers/grade_form.html', context)


@login_required
def grade_delete(request, grade_id):

    grade = get_object_or_404(Grade, id=grade_id)

    if grade.teacher != request.user:
        messages.error(request, 'Вы можете удалять только свои оценки!')
        return redirect('teachers:student_detail', student_id=grade.student.id)

    student_id = grade.student.id

    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Оценка удалена!')
        return redirect('teachers:student_detail', student_id=student_id)

    context = {
        'grade': grade,
    }

    return render(request, 'teachers/grade_delete.html', context)