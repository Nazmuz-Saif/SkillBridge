from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.applyjob, name='apply_job'),
    path('save/<int:job_id>/', views.savejob, name='save_job'),
]