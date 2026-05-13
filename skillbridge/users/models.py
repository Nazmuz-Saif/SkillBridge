from django.db import models
from django.contrib.auth.models import User


class FreelancerProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    universityname = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=200, blank=True)
    skills = models.TextField()
    experience = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    portfolio_link = models.URLField(blank=True)
    githublink = models.URLField(blank=True)
    linkedinlink = models.URLField(blank=True)
    profileimage = models.ImageField(upload_to='media/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    nidnumber = models.CharField(max_length=50)
    createdat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClientProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    companyname = models.CharField(max_length=200,blank=True)
    companydescription = models.TextField(blank=True)
    website = models.URLField(blank=True)
    profileimage = models.ImageField(upload_to='media/', blank=True, null=True)
    nidnumber = models.CharField(max_length=50)
    createdat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name