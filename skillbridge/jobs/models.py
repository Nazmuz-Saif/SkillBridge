from django.db import models
from django.contrib.auth.models import User


class JobCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(models.Model):

    EXPERIENCE_LEVEL_CHOICES = (
        ('entry', 'Entry Level'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    )

    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('remote', 'Remote'),
        ('contract', 'Contract'),
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    category = models.ForeignKey(
        JobCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    skills_required = models.ManyToManyField(Skill, blank=True)

    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='entry'
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='remote'
    )

    budget_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    budget_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    deadline = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):

    status_choicce = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    cover_letter = models.TextField()
    proposed_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=20, choices=status_choicce, default='pending')

    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('freelancer', 'job')
    
    def __str__(self):
        return f"{self.freelancer.username} - {self.job.title}"


class SavedJob(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('freelancer', 'job')

    def __str__(self):
        return f"{self.freelancer.username} - {self.job.title}"



class Contract(models.Model):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_contracts')

    application = models.OneToOneField(Application, on_delete=models.CASCADE)

    agreed_budget = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    started_at = models.DateTimeField(auto_now_add=True)