from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="accounts.signup"),
    path("login/", views.login, name="accounts.login"),
    path("logout/", views.logout, name="accounts.logout"),
    path(
        "notifications/", views.recruiter_notifications, name="accounts.notifications"
    ),
    path(
        "notifications/<int:pk>/read/",
        views.mark_notification_read,
        name="accounts.mark_notification_read",
    ),
    path(
        "oauth/google/login",
        views.google_oauth_start_login,
        name="google_oauth_start_login",
    ),
    path(
        "oauth/google/",
        views.google_oauth_start,
        name="google_oauth_start",
    ),
    path("oauth/callback/", views.google_oauth_callback, name="google_oauth_callback"),
    path("role-selection/", views.role_selection, name="role_selection"),
]
