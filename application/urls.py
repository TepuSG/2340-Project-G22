from django.urls import path
from . import views
urlpatterns = [
    path('apply/<int:id>/', views.apply_to_job, name='apply_to_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
]
