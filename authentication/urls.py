from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from authentication import candy

urlpatterns = [
    *candy.path('', views.home, name="home"),
    path('auth_login', views.auth_login, name="auth_login"),
    path('register', views.register, name="register"),
    path('signout', views.signout, name="signout"),
    path('location', views.location, name="location"),
    path('viewProfile', views.viewProfile, name="viewProfile"),
    path('requestForm', views.requestForm, name="requestForm"),
    path('send_notification/', views.send_notification, name='send_notification'),
    path('xxnetwork', views.xxnetwork, name='xxnetwork')
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)