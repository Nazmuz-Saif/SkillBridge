from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from jobs.models import Application, Job
from users.models import FreelancerProfile, ClientProfile
from .models import Review


# CLIENT SHOWS FREELANCERS
@login_required
def frereview(request):

    apps = Application.objects.filter(
        job__client=request.user.clientprofile,
        status='accepted'
    )

    return render(request, 'review/frereview.html', {
        'apps': apps
    })


@login_required
def give_review(request, email, job_id):

    user = User.objects.get(email=email)

    freelancer = FreelancerProfile.objects.get(user=user)

    job = Job.objects.get(id=job_id)

    if request.method == "POST":

        Review.objects.create(
            client=request.user.clientprofile,
            freelancer=freelancer,
            job=job,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

        return redirect('frereview')

    return render(request, 'review/clintreview.html', {
        'freelancer': freelancer,
        'job': job
    })


# FREELANCER SHOWS CLIENTS
@login_required
def clientreview(request):

    apps = Application.objects.filter(
        freelancer=request.user,
        status='accepted'
    )

    return render(request, 'review/clientreview.html', {
        'apps': apps
    })

@login_required
def give_client_review(request, email, job_id):

    user = User.objects.get(email=email)

    client = ClientProfile.objects.get(user=user)

    job = Job.objects.get(id=job_id)

    freelancer = request.user.freelancerprofile

    if request.method == "POST":

        Review.objects.create(
            client=client,
            freelancer=freelancer,
            job=job,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

        return redirect('clientreview')

    return render(request, 'review/give_client_review.html', {
        'client': client,
        'job': job
    })