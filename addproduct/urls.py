
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='addproduct'

urlpatterns = [
    path('/json/ajax/', views.create_product, name='create_product'),
    path('json/', views.show_json, name="show_json"),
    path('/katalog/add/', views.show_product, name='show_product'), 
    path('details/',views.product_details, name='product_details'),
    path('show_details/<int:id>/',views.show_details, name='show_details'),
    path('delete_product/<int:id>/', views.delete_product, name="delete_product"),
    path('jsonall/', views.show_json_all, name="show_json_all"),
    path('/create_product_flutter/', views.create_product_flutter, name="create_product_flutter"),
    path('/create_product_flutter2/', views.create_product_flutter2, name="create_product_flutter2"),
    path('/show_json_kategori/<kategori_id>/', views.show_json_kategori, name="show_json_kategori"),
]

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
