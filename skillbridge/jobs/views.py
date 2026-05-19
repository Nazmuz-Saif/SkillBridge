from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application, SavedJob, Skill, JobCategory
from .forms import JobForm
from users.models import FreelancerProfile
from django.contrib.auth.decorators import login_required
from .models import Job, Application, SavedJob

@login_required
def post_job(request):

    categories = JobCategory.objects.all()
    skills = Skill.objects.all()

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')

        category_id = request.POST.get('category')

        budget_min = request.POST.get('budget_min')
        budget_max = request.POST.get('budget_max')

        deadline = request.POST.get('deadline')

        experience_level=request.POST.get('experience_level'),
        job_type=request.POST.get('job_type'),

        category = JobCategory.objects.get(id=category_id)

        job = Job.objects.create(
            client=request.user,
            title=title,
            description=description,
            category=category,
            budget_min=budget_min,
            budget_max=budget_max,
            deadline=deadline,
            experience_level=experience_level,
            job_type=job_type,
        )

        selected_skills = request.POST.getlist('skills')

        job.skills_required.set(selected_skills)

        return redirect('clientdashboard')

    context = {
        'categories': categories,
        'skills': skills,
    }

    return render(request, 'jobs/post_job.html', context)


@login_required
def job_list(request):

    jobs = Job.objects.filter(is_active=True).order_by('-created_at')

    applied_jobs = Application.objects.filter(
        freelancer=request.user
    ).values_list('job_id', flat=True)

    saved_jobs = SavedJob.objects.filter(
        freelancer=request.user
    ).values_list('job_id', flat=True)

    context = {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
        'saved_jobs': saved_jobs,
    }

    return render(request, 'jobs/job_list.html', context)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_applied = Application.objects.filter(
        freelancer=request.user,
        job=job
    ).exists()
    if not already_applied:
        Application.objects.create(
            freelancer=request.user,
            job=job
        )
    return redirect('job_list')

@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_saved = SavedJob.objects.filter(
        freelancer=request.user,
        job=job
    ).exists()
    if not already_saved:
        SavedJob.objects.create(
            freelancer=request.user,
            job=job
        )
    return redirect('job_list')

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

@login_required
def client_jobs(request):
    jobs = Job.objects.filter(client=request.user).order_by('-created_at')

    return render(request, 'jobs/client_jobs.html', {
        'jobs': jobs
    })


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, client=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('client_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {
        'form': form,
        'job': job
    })

@login_required
def job_applications(request):

    applications = Application.objects.filter(
        job__client=request.user
    ).order_by('-applied_at')

    return render(request, 'jobs/job_applications.html', {
        'applications': applications
    })


@login_required
def update_application_status(request, app_id, status):

    application = get_object_or_404(
        Application,
        id=app_id
    )

    if application.job.client != request.user:
        return redirect('clientdashboard')

    valid_status = ['accepted', 'rejected', 'completed']

    if status in valid_status:
        application.status = status
        application.save()

    return redirect('job_applications')