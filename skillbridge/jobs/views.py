from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application, SavedJob

@login_required

def freelancer_dashboard(request):

    app_qs = Application.objects.filter(freelancer=request.user)
    saved_qs = SavedJob.objects.filter(freelancer=request.user)

    context = {
        'total_applications': app_qs.count(),
        'pending_applications': app_qs.filter(status='pending').count(),
        'accepted_jobs': app_qs.filter(status='accepted').count(),
        'rejected_jobs': app_qs.filter(status='rejected').count(),
        'saved_jobs': saved_qs.count(),
    }

    return render(request, 'users/freelencerdashboard.html', context)


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # prevent duplicate application
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
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    saved, created = SavedJob.objects.get_or_create(
        job=job,
        freelancer=request.user
    )

    return redirect('freelencerdashboard')
