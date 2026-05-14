from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application, SavedJob, Skill, JobCategory
from users.models import FreelancerProfile


@login_required
def post_job(request):

    categories = JobCategory.objects.all()
    skills = Skill.objects.all()

    if request.method == "POST":

        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        budget_min = request.POST.get('budget_min')
        budget_max = request.POST.get('budget_max')
        selected_skills = request.POST.getlist('skills')
        category = JobCategory.objects.get(id=category_id)
        deadline = request.POST.get('deadline')
        job = Job.objects.create(
            client=request.user,
            title=title,
            description=description,
            category=category,
            budget_min=budget_min,
            budget_max=budget_max,
            deadline=deadline
        )

        job.skills_required.set(selected_skills)
        skills = request.POST.getlist('skills')
        return redirect('clientdashboard')

    context = {
        'categories': categories,
        'skills': skills,
    }

    return render(request, 'jobs/post_job.html', context)

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

@login_required
def client_jobs(request):

    jobs = Job.objects.filter(
        client=request.user
    ).order_by('-created_at')

    return render(request, 'jobs/client_jobs.html', {
        'jobs': jobs
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
        id=app_id,
        job__client=request.user
    )

    application.status = status
    application.save()

    return redirect('job_applications')