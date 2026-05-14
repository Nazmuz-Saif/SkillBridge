from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('freelancer-dashboard/', views.freelancerdashboard, name='freelencerdashboard'),
    path('client-dashboard/', views.clientdashboard, name='clientdashboard'),
    path('freelancer-profile/',views.freelancer_profile,name='freelancerprofile'),
    path('client-profile/', views.client_profile, name='clientprofile'),
    path('find-talents/',views.find_talents,name='findtalents'),
]