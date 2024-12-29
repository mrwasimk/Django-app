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

class Students(models.Model):
    sname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    dob= models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    photo = models.ImageField(default='default.png', upload_to='profile_pics')

class Module(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    credit = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length= 100)
    availability= models.BooleanField(default=True)
    register = models.CharField(max_length= 100, blank=True)
    registered_users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

    
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    registerdate= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.module.name}"
