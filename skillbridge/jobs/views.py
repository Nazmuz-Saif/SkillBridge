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
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

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