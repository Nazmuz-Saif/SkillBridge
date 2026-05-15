from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job
from users.models import FreelancerProfile

class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='reviews')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.client} -> {self.freelancer.name}"