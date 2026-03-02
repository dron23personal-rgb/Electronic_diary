from django.urls import path
from .views import (
    teacher_dashboard,
    student_list,
    student_detail,
    student_create,
    student_edit,
    student_delete,
    add_grade,
    grade_delete,
    grade_create,
    grade_edit,
)

app_name = 'teachers'

urlpatterns = [
    path('', teacher_dashboard, name='dashboard'),

    path('students/', student_list, name='student_list'),
    path('students/create/', student_create, name='student_create'),
    path('students/<int:student_id>/', student_detail, name='student_detail'),
    path('students/<int:student_id>/edit/', student_edit, name='student_edit'),
    path('students/<int:student_id>/delete/', student_delete, name='student_delete'),

    path('students/<int:student_id>/add-grade/', add_grade, name='add_grade'),
    path('grades/<int:grade_id>/delete/', grade_delete, name='grade_delete'),

    path('grade/create/', grade_create, name='grade_create'),
    path('grade/<int:grade_id>/edit/', grade_edit, name='grade_edit'),
]