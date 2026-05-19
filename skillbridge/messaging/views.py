from django.shortcuts import render, redirect
from .models import Message
from jobs.models import Job

def nochat(request):
    return render(request,'chat/nochat.html')

def chat(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            Message.objects.create(job=job,sender=request.user,text=text)
        return redirect('chat',job_id=job.id)
    messages = Message.objects.filter(job=job).order_by('timestamp')
    context = {
        'job': job,
        'messages': messages
    }
    return render(request,'chat/chat.html',context)