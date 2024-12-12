from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from django.core.validators import EmailValidator

class Issue(models.Model):
    type = models.CharField(max_length=100, choices=[('Hardware', 'Hardware'), ('Software', 'Software')])
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default=False)
    details = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(User, related_name='issues', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} Issue in {self.room}'

    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs={'pk': self.pk})


class Contact(forms.Form):
    Firstname = forms.CharField(max_length=50)
    Surename = forms.CharField(max_length=50)
    Email = forms.CharField(validators=[EmailValidator()])
    Address = forms.CharField(max_length=50)
    Phonenumber = forms.CharField(max_length=11)
    Message = forms.CharField(widget=forms.Textarea)

class Module(forms.Form):
    modulename = forms.CharField(max_length=50)
    Code = forms.CharField(max_length=50)
    Credit = forms.CharField(max_length=50)
    AddCategory = forms.CharField(max_length=50)
    Phonenumber = forms.CharField(max_length=11)
    Description = forms.CharField(widget=forms.Textarea)
    Availability = forms.CharField(max_length=50)
    Course = forms.CharField(max_length=50)

class Contact(forms.Form):
    Firstname = forms.CharField(max_length=50)
    Surename = forms.CharField(max_length=50)
    Email = forms.CharField(validators=[EmailValidator()])
    Address = forms.CharField(max_length=50)
    Phonenumber = forms.CharField(max_length=11)
    Message = forms.CharField(widget=forms.Textarea)