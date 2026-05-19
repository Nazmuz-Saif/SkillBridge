from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Message(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username