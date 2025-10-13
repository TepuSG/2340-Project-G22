from django.urls import path
from . import views

urlpatterns = [
    path('', views.available_jobs, name='jobs.index'),
    path('filters', views.filters, name='jobs.filters'),
    path('post/', views.post_job, name='post_job'),
]
