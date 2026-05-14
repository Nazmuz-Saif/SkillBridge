from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import FreelancerProfileForm, SignupForm
from .models import FreelancerProfile, ClientProfile
from jobs.models import Application, SavedJob


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

# @login_required
# def freelancerdashboard(request):
#     profile = FreelancerProfile.objects.get(user=request.user)

#     return render(request, 'users/freelencerdashboard.html', {
#         'profile': profile,
#         'role': 'freelancer'
#     })

@login_required
def clientdashboard(request):
    profile = ClientProfile.objects.get(user=request.user)

    return render(request, 'users/clintdashboard.html', {
        'profile': profile,
        'role': 'client'
    })


@login_required
def freelancerdashboard(request):

    app_qs = Application.objects.filter(freelancer=request.user)
    saved_qs = SavedJob.objects.filter(freelancer=request.user)

    recent_apps = app_qs.select_related('job').order_by('-applied_at')[:5]
    recent_saved = saved_qs.select_related('job').order_by('-saved_at')[:5]

    context = {
        'user_name': request.user.username,

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
def freelancer_profile(request):
    profile = FreelancerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('freelancerprofile')

    else:
        form = FreelancerProfileForm(instance=profile)

    skills = profile.skills.split(',') if profile.skills else []
    skills = [s.strip() for s in skills if s.strip()]

    return render(request, 'users/freelancerprofile.html', {
        'profile': profile,
        'skills': skills,
        'form': form,
        'role': 'freelancer'
    })



