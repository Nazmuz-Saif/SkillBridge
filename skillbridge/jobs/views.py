from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application, SavedJob


@login_required
def post_job(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        budget = request.POST['budget']

        job = Job.objects.create(
            client=request.user,
            title=title,
            description=description,
            budget=budget
        )

        return redirect('clientdashboard')

    return render(request, 'jobs/post_job.html')

def job_list(request):

    jobs = Job.objects.filter(is_active=True).order_by('-created_at')

    context = {
        'jobs': jobs
    }

    return render(request, 'jobs/job_list.html', context)

@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == "POST":
        cover_letter = request.POST['cover_letter']

        Application.objects.create(
            job=job,
            freelancer=request.user,
            cover_letter=cover_letter
        )

        return redirect('freelencerdashboard')

    return render(request, 'jobs/apply.html', {'job': job})

@login_required
def savejob(request, job_id):
    job = Job.objects.get(id=job_id)

    SavedJob.objects.get_or_create(
        job=job,
        freelancer=request.user
    )

    return redirect('freelencerdashboard')

@login_required
def my_applications(request):

    applications = Application.objects.filter(
        freelancer=request.user
    ).select_related('job').order_by('-applied_at')

    return render(request, 'jobs/my_applications.html', {
        'applications': applications
    })

@login_required
def saved_jobs(request):

    saved = SavedJob.objects.filter(
        freelancer=request.user
    ).select_related('job').order_by('-saved_at')

    return render(request, 'jobs/saved_jobs.html', {
        'saved_jobs': saved
    })

@login_required
def save_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    SavedJob.objects.get_or_create(
        freelancer=request.user,
        job=job
    )

    return redirect('saved_jobs')