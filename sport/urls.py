from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/<int:schedule_id>/attendance/', views.mark_attendance, name='mark_attendance'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/<int:pk>/', views.exercise_detail, name='exercise_detail'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('ai/chat/', views.ai_chat, name='ai_chat'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # ---- Admin User Management ----
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/add/', views.admin_user_add, name='admin_user_add'),
    path('admin/users/<int:pk>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin/attendance/', views.admin_attendance_list, name='admin_attendance_list'),

    path('admin/schedules/', views.admin_schedule_list_view, name='admin_schedule_list'),
    path('admin/schedules/add/', views.admin_schedule_add, name='admin_schedule_add'),
    path('admin/schedules/<int:pk>/edit/', views.admin_schedule_edit, name='admin_schedule_edit'),
    path('admin/schedules/<int:pk>/delete/', views.admin_schedule_delete, name='admin_schedule_delete'),

    path('admin/exercises/', views.admin_exercise_list_view, name='admin_exercise_list'),
    path('admin/exercises/add/', views.admin_exercise_add, name='admin_exercise_add'),
    path('admin/exercises/<int:pk>/edit/', views.admin_exercise_edit, name='admin_exercise_edit'),
    path('admin/exercises/<int:pk>/delete/', views.admin_exercise_delete, name='admin_exercise_delete'),

    # ---- Admin Blog Management ----
    path('admin/blogs/', views.admin_blog_list_view, name='admin_blog_list'),
    path('admin/blogs/add/', views.admin_blog_add, name='admin_blog_add'),
    path('admin/blogs/<int:pk>/edit/', views.admin_blog_edit, name='admin_blog_edit'),
    path('admin/blogs/<int:pk>/delete/', views.admin_blog_delete, name='admin_blog_delete'),

]