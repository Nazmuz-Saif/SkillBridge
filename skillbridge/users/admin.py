from django.contrib import admin
from .models import ClientProfile, FreelancerProfile

admin.site.register(FreelancerProfile)
admin.site.register(ClientProfile)
