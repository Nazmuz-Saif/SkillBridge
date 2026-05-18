from django.shortcuts import render

from jobs.models import Job
from users.models import FreelancerProfile

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def guest_job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'core/alljob.html', {'jobs': jobs})

def guest_talents_list(request):
    freelancers = FreelancerProfile.objects.all().order_by('-createdat')
    return render(request, 'core/alltalent.html', {'freelancers': freelancers})

