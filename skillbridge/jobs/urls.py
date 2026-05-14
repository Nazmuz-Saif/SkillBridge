from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('save/<int:job_id>/', views.savejob, name='save_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),
    path('save-job/<int:job_id>/', views.save_job, name='save_job'),
]