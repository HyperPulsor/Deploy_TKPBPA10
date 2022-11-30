from django.urls import path
from landing.views import *

app_name = 'landing'

urlpatterns = [
    path('landing/', show_landing, name='show_landing'),
    path('/json/', show_json, name='show_json'),
]