from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from jobs.models import Application, Job
from users.models import FreelancerProfile, ClientProfile
from .models import Review


# CLIENT → FREELANCER LIST
@login_required
def frereview(request):

    client = ClientProfile.objects.filter(user=request.user).first()
    apps = Application.objects.filter(
    job__client=request.user,
    status='accepted'
)

    return render(request, 'review/frereview.html', {
        'apps': apps
    })


# CLIENT → GIVE REVIEW
@login_required
def give_review(request, email, job_id):

    user = User.objects.get(email=email)

    freelancer = FreelancerProfile.objects.get(user=user)

    job = Job.objects.get(id=job_id)

    client = ClientProfile.objects.get(user=request.user)

    if request.method == "POST":

        Review.objects.create(
            client=client,
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


# FREELANCER → CLIENT LIST
@login_required
def clientreview(request):

    freelancer = FreelancerProfile.objects.get(user=request.user)

    apps = Application.objects.filter(
        freelancer=freelancer,
        status='accepted'
    )

    return render(request, 'review/clientreview.html', {
        'apps': apps
    })


# FREELANCER → GIVE CLIENT REVIEW
@login_required
def give_client_review(request, email, job_id):

    user = User.objects.get(email=email)

    client = ClientProfile.objects.get(user=user)

    job = Job.objects.get(id=job_id)

    freelancer = FreelancerProfile.objects.get(user=request.user)

    if request.method == "POST":

        Review.objects.create(
            client=client,
            freelancer=freelancer,
            job=job,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

        return redirect('clientreview')

    return render(request, 'review/client_review_form.html', {
        'client': client,
        'job': job
    })