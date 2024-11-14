from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {'u_form': u_form, 'p_form': p_form, 'title': 'StudentProfile'}
    return render(request, 'users/profile.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'Student Profile'})
# Create your views here.
