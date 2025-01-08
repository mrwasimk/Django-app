from django.shortcuts import render
from django.http import HttpResponse
from .models import Issue
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from .models import Contact
from django.core.mail import EmailMessage
import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import Module, Students, Registration
from django.http import HttpResponse
from datetime import datetime


def home(request):
    
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = '1f9c0d6aa16a263969692d60d8801e9e'

    for city in cities:
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json()
        weather = {
            'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description']
        }
        weather_data.append(weather)  # Add each city's data to the list

    return render(request, 'itreporting/home.html', {'title': 'Homepage', 'weather_data': weather_data})


def course_list(request):
    courses = Module.objects.all()
    return render(request, 'itreporting/course_list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Module, pk=pk)
    registrations = Registration.objects.filter(module=course)
    if request.method == "POST":
        if not course.availability:
            messages.error(request, "This course is currently unavailable for registration.")
        elif Registration.objects.filter(user=request.user, module=course).exists():
            messages.error(request, "You are already registered for this course.")
        else:
            Registration.objects.create(user=request.user, module=course, registerdate=datetime.now())
            messages.success(request, f"You have successfully registered for {course.name}.")
            return redirect('itreporting:course-detail', pk=pk)
    return render(request, 'itreporting/course_detail.html', {'course': course, 'registrations': registrations})


'''def course_detail(request, pk):
    course = get_object_or_404(Module, pk=pk)
    return render(request, 'itreporting/course_detail.html', {'course': course})'''

@login_required
def registration_detail(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'itreporting/registration_detail.html', {'registrations': registrations})

def student_list(request):
    students = Students.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def student_detail(request, pk):
    student = get_object_or_404(Students, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

def registration_list(request):
    registrations = Registration.objects.all()
    return render(request, 'itreporting/registration_list.html', {'registrations': registrations})


'''def registration_detail(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    return render(request, 'registrations/registration_detail.html', {'registration': registration})'''

#def contact(request):
    #return render(request, 'itreporting/contact.html', {'title': 'Contact'})

def about(request):
    return render(request, 'itreporting/about.html', {'title': 'About'})

def report(request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

def contact(request):
    if request.method == "POST":
        form = Contact(request.POST)
        if form.is_valid():
            Firstname = form.cleaned_data["Firstname"]
            Surename = form.cleaned_data["Surename"]
            Email = form.cleaned_data["Email"]
            Address = form.cleaned_data["Address"]
            Phonenumber = form.cleaned_data["Phonenumber"]
            Message = form.cleaned_data["Message"]
            email_message = EmailMessage(
                subject=f"Contact Form from {Firstname,Surename}",
                body=Message,
                from_email= Email,
                to=["noreply@SHU.com"],
                reply_to=[Email],
            )
            email_message.send()
            messages.success(request, "Your message has been received!")
            form = Contact() 

        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = Contact()

    return render(request, 'itreporting/contact.html', {'form': form, 'title': 'Contact'})

class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'


class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 10 # Optional pagination


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['type', 'room', 'urgent', 'details']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

#class PostUpdateView(LoginRequiredMixin, UpdateView):
    #model = Issue
    #fields = ['type', 'room', 'details']


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['type', 'room', 'details']
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = '/report'
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author
    
