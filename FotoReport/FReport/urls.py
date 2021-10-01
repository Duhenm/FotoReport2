from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admins', views.admins, name='admins'),
    path('FO', views.FO, name='FO'),
    path('', views.main, name='main'),
    path('main', views.main),
    path('admins_add', views.admins_add, name='admins_add'),
    path('simple_upload', views.simple_upload, name='simple_upload'),
    path('foto_add', views.foto_add, name='foto_add'),
    path('click_copy_files', views.click_copy_files, name='click_copy_files'),
    path('create_sc', views.create_sc, name='create_sc'),
    path('montag/<id>', views.montag2, name='montag2'),
    path('montag/start/<id>', views.start_report, name='start_report'),
    path('montag/start/<id>/<clip>', views.start_report, name='start_report'),
    path('montag', views.montag, name='montag'),
    #path('montag/<id>', views.montag2, name='montag2'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)