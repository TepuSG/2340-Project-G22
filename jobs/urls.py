from django.urls import path
from . import views
from .views import JobUpdateView

urlpatterns = [
    path("", views.available_jobs, name="jobs.index"),
    path("filters", views.filters, name="jobs.filters"),
    path("post/", views.post_job, name="post_job"),
    path("<int:pk>/edit/", JobUpdateView.as_view(), name="edit_job"),
    path("my-jobs/", views.recruiter_jobs, name="recruiter_jobs"),
    path(
        "job/<int:job_id>/pipeline/",
        views.job_applicants_pipeline,
        name="job_applicants_pipeline",
    ),
    path(
        "application/<int:application_id>/status/<str:new_status>/",
        views.update_application_status,
        name="update_application_status",
    ),
    path("location-search/", views.location_search, name="location_search"),
    path(
        "search-suggestions/",
        views.job_search_suggestions,
        name="job_search_suggestions",
    ),
]
