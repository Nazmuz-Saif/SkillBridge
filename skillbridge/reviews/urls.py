from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('clintreviews/', views.clintreview, name ='clintreview'),
    path('frereviews/', views.frereview, name ='frereview'),
]