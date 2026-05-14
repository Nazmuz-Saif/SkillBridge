from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('save/<int:job_id>/', views.savejob, name='save_job'),
    path('jobs/', views.job_list, name='job_list'),
]