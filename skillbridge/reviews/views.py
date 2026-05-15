from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def frereview(request):
    worked_freelancers = [
        {
            'freelancer': {'id': 1, 'name': 'John Doe', 'profileimage': None},
            'project_title': 'Web Development'
        },
        {
            'freelancer': {'id': 2, 'name': 'Alex Smith', 'profileimage': None},
            'project_title': 'App Design'
        }
    ]
    
    context = {
        'worked_freelancers': worked_freelancers
    }
    return render(request, 'review/frereview.html', context)


@login_required
def clintreview(request, freelancer_id):
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
    context = {}
    return render(request, 'review/clintreview.html', context)