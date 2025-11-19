from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='recommended.index'),
    path('recruiter/overview/', views.recruiter_overview, name='recommended.overview'),
    path('recruiter/candidates/search/', views.candidate_search, name='recommended.candidate_search'),
    path('recruiter/saved-searches/', views.saved_searches_list, name='recommended.saved_searches'),
    path('recruiter/saved-searches/save/', views.save_search, name='recommended.save_search'),
    path('recruiter/saved-searches/delete/<int:pk>/', views.delete_saved_search, name='recommended.delete_saved_search'),

]