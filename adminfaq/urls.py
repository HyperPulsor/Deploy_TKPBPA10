from django.urls import path
from adminfaq.views import *

app_name = 'faq'

urlpatterns = [
    path('', show_faq, name='show_faq'),
    path('create_faq/', create_faq, name='create_faq'),
    path('json/', show_json, name='show_json'),
    path('create_faq_flutter/', create_faq_flutter, name= 'create_faq_flutter'),
    path('delete_faq/<int:id>/', delete_faq, name='delete_faq'),
]
