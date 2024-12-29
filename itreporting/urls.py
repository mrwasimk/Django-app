from django.contrib import admin
from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
app_name = 'itreporting'

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),

    path('report/', PostListView.as_view(), name = 'report'),  
    path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
    path('issue/new', PostCreateView.as_view(), name = 'issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name = 'issue-update'),
    path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name = 'issue-delete'),
    
    path('courses/', views.course_list, name = 'course-list'),
    path('courses/<int:pk>', views.course_detail, name = 'course-detail'),
    path('student/', views.student_list, name = 'student-list'),
    path('student/<int:pk>', views.student_detail, name = 'student-detail'),  
    path('registration/', views.registration_list, name = 'registration-list'),
    path('registration/<int:pk>', views.registration_detail, name = 'registration-detail'),
]
