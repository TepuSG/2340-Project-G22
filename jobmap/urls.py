from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jobmap.index'),
    path('update_distance/', views.update_distance, name='jobmap.update_distance')
]
