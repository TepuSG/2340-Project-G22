from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'),
    path('search', views.search, name='home.search'),
    path('filters', views.filters, name='home.filters'),
]