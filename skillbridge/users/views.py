from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import FreelancerProfileForm, SignupForm
from .models import FreelancerProfile, ClientProfile
from jobs.models import Job, Application, SavedJob ,JobCategory
from django.db.models import Q
def signup(request):
    form=SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            if User.objects.filter(username=email).exists():
                return render(request, 'users/signup.html', {'form': form, 'error': 'Email already exists'})
            user = User.objects.create_user(username=email,email=email,password=password)
            if role == 'freelancer':
                FreelancerProfile.objects.create(user=user,name=name,email=email)
            else:
                ClientProfile.objects.create(user=user,name=name,email=email)
            return redirect('login')
    return render(request, 'users/signup.html', {'form': form})


def loginview(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            if FreelancerProfile.objects.filter(user=user).exists():
                request.session['role'] = 'freelancer'
                return redirect('freelencerdashboard')
            elif ClientProfile.objects.filter(user=user).exists():
                request.session['role'] = 'client'
                return redirect('clientdashboard')
        return render(request, 'users/login.html', {
            'error': 'Invalid credentials'
        })
    return render(request, 'users/login.html')


def logoutview(request):
    logout(request)
    return redirect('home')


@login_required
def clientdashboard(request):
    profile = ClientProfile.objects.get(user=request.user)

    return render(request, 'users/clintdashboard.html', {
        'profile': profile,
        'role': 'client'
    })


@login_required
def freelancerdashboard(request):
    profile = FreelancerProfile.objects.get(user=request.user)
    app_qs = Application.objects.filter(freelancer=request.user)
    saved_qs = SavedJob.objects.filter(freelancer=request.user)

    recent_apps = app_qs.select_related('job').order_by('-applied_at')[:5]
    recent_saved = saved_qs.select_related('job').order_by('-saved_at')[:5]

    context = {
        'profile': profile,
        'role': 'freelancer',

        'total_applications': app_qs.count(),
        'pending_applications': app_qs.filter(status='pending').count(),
        'accepted_jobs': app_qs.filter(status='accepted').count(),
        'rejected_jobs': app_qs.filter(status='rejected').count(),

        'saved_jobs': saved_qs.count(),

        'recent_applications': recent_apps,
        'recent_saved_jobs': recent_saved,
    }

    return render(request, 'users/freelencerdashboard.html', context)

@login_required
def clientdashboard(request):
    profile = ClientProfile.objects.get(user=request.user)
    job_qs = Job.objects.filter(client=request.user)

    app_qs = Application.objects.filter(job__client=request.user)

    recent_jobs = job_qs.order_by('-created_at')[:5]

    recent_apps = app_qs.select_related('job', 'freelancer').order_by('-applied_at')[:5]

    context = {
        'profile': profile,
        'role': 'client',

        'total_jobs': job_qs.count(),
        'active_jobs': job_qs.filter(is_active=True).count(),
        'closed_jobs': job_qs.filter(is_active=False).count(),

        'total_applications': app_qs.count(),
        'hired_freelancers': app_qs.filter(status='accepted').count(),
        'recent_jobs': recent_jobs,
        'recent_applications': recent_apps,
    }

    return render(request, 'users/clintdashboard.html', context)

@login_required
def freelancer_profile(request):

    profile = FreelancerProfile.objects.get(user=request.user)

    if request.method == 'POST':

        profile.name = request.POST.get('name')
        profile.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.universityname = request.POST.get('universityname')
        profile.degree = request.POST.get('degree')
        profile.skills = request.POST.get('skills')
        profile.experience = request.POST.get('experience')
        profile.bio = request.POST.get('bio')
        profile.portfolio_link = request.POST.get('portfolio_link')
        profile.githublink = request.POST.get('githublink')
        profile.linkedinlink = request.POST.get('linkedinlink')

        if request.FILES.get('profileimage'):
            profile.profileimage = request.FILES.get('profileimage')

        profile.save()

        return redirect('freelancerprofile')

    return render(request, 'users/freelancerprofile.html', {
        'profile': profile,
        'role': 'freelancer'
    })

@login_required
def client_profile(request):

    profile = ClientProfile.objects.get(user=request.user)

    if request.method == 'POST':

        profile.name = request.POST.get('name')
        profile.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.companyname = request.POST.get('companyname')
        profile.companydescription = request.POST.get('companydescription')
        profile.website = request.POST.get('website')
        profile.nidnumber = request.POST.get('nidnumber')

        if request.FILES.get('profileimage'):
            profile.profileimage = request.FILES.get('profileimage')

        profile.save()

        return redirect('clientprofile')

    return render(request, 'users/clientprofile.html', {
        'profile': profile,
        'role': 'client'
    })

@login_required
def find_talents(request):

    freelancers = FreelancerProfile.objects.all().order_by('-createdat')

    context = {
        'freelancers': freelancers,
        'role': 'client'
    }

    return render(request, 'users/find_talents.html', context)


@login_required
def search(request):
    query = request.GET.get('q', '')

    jobs = Job.objects.filter(title__icontains=query)

    categories = JobCategory.objects.filter(name__icontains=query)

    clients = ClientProfile.objects.filter(
        Q(name__icontains=query) | Q(companyname__icontains=query)
    )

    freelancers = FreelancerProfile.objects.filter(
        Q(name__icontains=query) | Q(skills__icontains=query)
    )

    return render(request, 'users/search.html', {
        'query': query,
        'jobs': jobs,
        'categories': categories,
        'clients': clients,
        'freelancers': freelancers,
    })
