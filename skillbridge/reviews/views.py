from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from jobs.models import Application, Job
from .models import Review
from users.models import FreelancerProfile

@login_required
def frereview(request):

    apps = Application.objects.filter(
        job__client=request.user,
        status='accepted'
    ).select_related('job', 'freelancer')

    pending = []

    for app in apps:
        freelancer = app.freelancer.freelancerprofile

        exists = Review.objects.filter(
            client=request.user,
            freelancer=freelancer,
            job=app.job
        ).exists()

        if not exists:
            pending.append(app)

    return render(request, 'review/frereview.html', {
        'apps': pending
    })

@login_required
def give_review(request, freelancer_id, job_id):

    freelancer = get_object_or_404(FreelancerProfile, id=freelancer_id)
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        Review.objects.create(
            client=request.user,
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

