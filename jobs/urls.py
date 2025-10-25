from django.urls import path
from . import views
from .views import JobUpdateView

urlpatterns = [
    path('', views.available_jobs, name='jobs.index'),
    path('filters', views.filters, name='jobs.filters'),
    path('post/', views.post_job, name='post_job'),
    path('<int:pk>/edit/', JobUpdateView.as_view(), name='edit_job'),
    path('my-jobs/', views.recruiter_jobs, name='recruiter_jobs'),
]
