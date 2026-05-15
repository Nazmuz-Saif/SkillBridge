from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('reviews/', views.frereview, name='frereview'),
    path('review/<int:freelancer_id>/<int:job_id>/', views.give_review, name='clintreview'),
]