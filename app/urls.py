from django.urls import path
from django.contrib import admin
from django.urls import path, include


from django.conf.urls.static import static
from django.conf import settings

from app import views

urlpatterns = [
    path('', views.simple_upload),
]