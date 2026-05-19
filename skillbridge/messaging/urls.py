from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('nochat',views.nochat,name='nochat'),
    path('chat/<int:job_id>/',views.chat,name='chat'),
]