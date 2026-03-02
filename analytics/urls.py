from django.urls import path
from .views import statistics_view

app_name = 'analytics'

urlpatterns = [
    path('statistics/', statistics_view, name='statistics'),
]