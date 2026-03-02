from django.contrib import admin
from .models import TeacherProfile

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'room_number')
    filter_horizontal = ('subjects',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')