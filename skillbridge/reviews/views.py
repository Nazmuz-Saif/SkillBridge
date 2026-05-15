from django.shortcuts import render
def clintreview (request):
    return render(request, 'review/clintreview.html')
def frereview (request):
    return render(request, 'review/frereview.html')
# Create your views here.
