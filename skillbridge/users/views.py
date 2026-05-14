from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import FreelancerProfileForm, SignupForm
from .models import FreelancerProfile, ClientProfile


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
    return render(request, 'users/login.html')


def logoutview(request):
    logout(request)
    return redirect('home')

@login_required
def freelancerprofile(request):
    profile = FreelancerProfile.objects.get(user=request.user)

    return render(request, 'users/freelencerdashboard.html', {
        'profile': profile,
        'role': 'freelancer'
    })

@login_required
def clientprofile(request):
    profile = ClientProfile.objects.get(user=request.user)

    return render(request, 'users/clintdashboard.html', {
        'profile': profile,
        'role': 'client'
    })


@login_required
def freelancer_profile(request):
    profile = FreelancerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FreelancerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            return redirect('freelancerprofile')
    else:
        form = FreelancerProfileForm(instance=profile)
    return render(request,'users/freelancerprofile.html',{
        'profile': profile,
        'form': form,
        'role':'freelancer'
    })