from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('freelancer-profile/', views.freelancerprofile, name='freelancerprofile'),
    path('client-profile/', views.clientprofile, name='clientprofile'),
]