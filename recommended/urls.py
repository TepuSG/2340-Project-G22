from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='recommended.index'),
    path('recruiter/overview/', views.recruiter_overview, name='recommended.overview'),

]