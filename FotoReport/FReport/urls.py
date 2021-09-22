from django.urls import path
from . import views

urlpatterns = [
    path('admins', views.admins, name='admins'),
    path('FO', views.FO, name='FO'),
    path('', views.main, name='main'),
    path('main', views.main),
    path('admins_add', views.admins_add, name='admins_add'),
    path('foto_add', views.foto_add, name='foto_add'),
]