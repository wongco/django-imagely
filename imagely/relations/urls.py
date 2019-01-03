# Equivalent to Express Router File
from django.urls import path

from . import views

# urls for /images routes

urlpatterns = [
    path('', views.images, name='images')
]