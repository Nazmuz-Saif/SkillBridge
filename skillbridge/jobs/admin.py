from django.contrib import admin
from .models import Job, Application, SavedJob, Skill, JobCategory, Contract

admin.site.register(Job)
admin.site.register(Application)
admin.site.register(SavedJob)
admin.site.register(Skill)
admin.site.register(JobCategory)
admin.site.register(Contract)