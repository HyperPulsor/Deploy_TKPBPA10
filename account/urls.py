from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('registerbuyer/', views.registerbuyer, name='registerbuyer'),
    path('registerseller/', views.registerseller, name='registerseller'),
    path('adminpage/', views.admin, name='adminpage'),
    path('buyer/', views.buyer, name='buyer'),
    path('seller/', views.seller, name='seller'),
    path('logout/', views.logout_user, name='logout'),
    path('donasi_barang/', views.donasi_barang, name='donasi_barang'),
    path('json/', views.show_json, name='show_json'),
    path('login_flutter/', views.login_flutter, name='login_flutter'),
    path('signup_flutter/', views.signup_flutter, name='signup_flutter'),
    path('logout_flutter/', views.logout_flutter, name='logout_flutter'),
    path('user/', views.get_user, name='user'),
    path('profile_json/', views.profile_json, name='profile_json'),
]