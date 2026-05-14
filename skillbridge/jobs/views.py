from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application, SavedJob



@login_required
def applyjob(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    already_applied = Application.objects.filter(
        job=job,
        freelancer=request.user
    ).exists()

    if not already_applied:
        Application.objects.create(
            job=job,
            freelancer=request.user,
            cover_letter=request.POST.get('cover_letter', ''),
            status='pending'
        )

    return redirect('freelencerdashboard')

@login_required
def savejob(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    SavedJob.objects.get_or_create(
        job=job,
        freelancer=request.user
    )
    return redirect('freelencerdashboard')