from django.urls import path
from . import views
from stockticker.dash_apps.finished_apps import simpleexample  # Don't delete - wont work without it!!!
urlpatterns = [
    path('', views.home, name='stockticker')
]
