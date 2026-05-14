from django.urls import path
from . import views


urlpatterns = [
    path('freelancer-dashboard/', views.freelancer_dashboard, name='freelencerdashboard'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('save/<int:job_id>/', views.save_job, name='save_job'),
]