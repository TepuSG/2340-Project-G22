from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("me/edit/", views.profile_edit, name="edit"),
    path("u/<str:username>/", views.profile_detail, name="detail"),
]
