from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('notifications/', views.recruiter_notifications, name='accounts.notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='accounts.mark_notification_read'),
]