from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jobmap.index'),
]
