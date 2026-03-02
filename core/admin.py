from django.contrib import admin
from .models import Student, Subject, Grade

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'group', 'birth_date', 'created_at')
    list_filter = ('group',)
    search_fields = ('full_name', 'group')
    date_hierarchy = 'birth_date'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'date', 'teacher')
    list_filter = ('subject', 'score', 'date', 'teacher')
    search_fields = ('student__full_name', 'subject__name', 'comment')
    date_hierarchy = 'date'