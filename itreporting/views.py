from django.shortcuts import render
from django.http import HttpResponse
from .models import Issue

def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome'})

def contact(request):
    return render(request, 'itreporting/contact.html', {'title': 'Contact'})

def about(request):
    return render(request, 'itreporting/about.html', {'title': 'About'})

def report(request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

def report(request): # Get all reported issues
    issues = Issue.objects.all() # Create a context dictionary to pass to the template
    context = {'issues': issues}
    return render(request, 'itreporting/report.html', context) # Render the report.html template with the context
# Create your views here.
