from django.shortcuts import render
from django.http import HttpResponse
from .models import Issue
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from .models import Contact
from django.core.mail import EmailMessage

def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome'})

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