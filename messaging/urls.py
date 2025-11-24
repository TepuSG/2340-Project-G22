from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('email/<str:username>/', views.send_email, name='send_email'),
    path('<str:username>/', views.conversation, name='conversation'),
]
