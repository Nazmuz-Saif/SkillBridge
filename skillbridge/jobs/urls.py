from django.urls import path
from . import views
from .views import job_applications, update_application_status

urlpatterns = [
    path('alljobs/', views.job_list, name='job_list'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),
    path('post-job/', views.post_job, name='post_job'),
    path('my-jobs/', views.client_jobs, name='client_jobs'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('job-applications/',job_applications,name='job_applications'),
    path('update-application-status/<int:app_id>/<str:status>/',update_application_status,name='update_application_status'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('save-job/<int:job_id>/', views.save_job, name='save_job'),
    path('application-status/<int:app_id>/<str:status>/',views.update_application_status,name='update_application_status'),
    path('delete-job/<int:job_id>/',views.delete_job,name='delete_job'),
]