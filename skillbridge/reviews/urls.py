from django.urls import path
from . import views

urlpatterns = [

    path(
        'frereview/',views.frereview,name='frereview'
    ),

    path(
        'give-review/<str:email>/<int:job_id>/',views.give_review,name='give_review'
    ),

    path(
        'clientreview/',views.clientreview,name='clientreview'
    ),

    path(
        'give-client-review/<str:email>/<int:job_id>/',views.give_client_review,name='give_client_review'
    ),

]
