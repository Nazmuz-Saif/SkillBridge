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

    recent_apps = app_qs.select_related('job').order_by('-id')[:5]
    recent_saved = saved_qs.select_related('job').order_by('-id')[:5]

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



