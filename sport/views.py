from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Count
from google import genai
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegisterForm, ScheduleForm, UserUpdateForm, ProfileUpdateForm, ExerciseForm, BlogPostForm
from .decorators import admin_required
from .models import AIConversation # Ensure this is used
from .models import (
    Profile,
    Schedule,
    Exercise,
    SportVideo,
    Attendance,
    BlogPost,
    Comment,
    Notification,
    Progress,
    Achievement,
    UserAchievement,
)



@login_required
@admin_required
def admin_dashboard(request):
    # Calculate User Activity (Last 7 Days)
    today = timezone.now().date()
    activity_labels = []
    activity_counts = []
    
    for i in range(6, -1, -1):
        day = today - timezone.timedelta(days=i)
        count = Profile.objects.filter(joined_date__date=day).count()
        activity_labels.append(day.strftime('%b %d'))
        activity_counts.append(count)

    context = {
        # Statistics
        'users_count': Profile.objects.count(),
        'schedules_count': Schedule.objects.count(),
        'exercises_count': Exercise.objects.count(),
        'blogs_count': BlogPost.objects.count(),
        'videos_count': SportVideo.objects.count(),
        'attendance_count': Attendance.objects.count(),
        'notifications_count': Notification.objects.count(),
        'achievements_count': Achievement.objects.count(),
        'progress_count': Progress.objects.count(),

        # Recent Data
        'recent_users': User.objects.select_related('profile').order_by('-date_joined')[:5],
        'recent_schedules': Schedule.objects.order_by('-created_at')[:5],
        'recent_blogs': BlogPost.objects.order_by('-created_at')[:5],

        # Chart Data
        'activity_labels': json.dumps(activity_labels),
        'activity_counts': json.dumps(activity_counts),
    }

    return render(request, 'sport/admin_dashboard.html', context)

    

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def landing(request):
    return render(request, 'sport/landing.html')


@login_required
def home(request):
    # Unified check for admin access
    is_admin = request.user.is_staff or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN')
    if is_admin:
        return redirect('admin_dashboard')

    today = timezone.now().date()

    schedules = Schedule.objects.filter(date=today)
    notifications = Notification.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]

    exercises = Exercise.objects.all()[:4]

    context = {
        'schedules': schedules,
        'notifications': notifications,
        'exercises': exercises,
    }

    return render(request, 'sport/home.html', context)



@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'sport/profile.html', {
        'profile': profile
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)

        # Security: Prevent non-admins from changing their own role
        if not request.user.is_staff and profile.role != 'ADMIN':
            p_form.fields.pop('role', None)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
        if not request.user.is_staff and profile.role != 'ADMIN':
            p_form.fields.pop('role', None)

    return render(request, 'sport/profile_form.html', {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Edit Profile'
    })


def schedule_list(request):
    schedules = Schedule.objects.all().order_by('date', 'start_time')
    return render(request, 'sport/schedule_list.html', {
        'schedules': schedules
    })

@login_required
@admin_required
def admin_schedule_add(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New schedule added successfully!")
            return redirect('admin_schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'sport/schedule_form.html', {'form': form, 'title': 'Add New Schedule'})

@login_required
@admin_required
def admin_schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule updated successfully!")
            return redirect('admin_schedule_list')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'sport/schedule_form.html', {'form': form, 'title': f'Edit Schedule: {schedule.title}'})

@login_required
@admin_required
def admin_schedule_delete(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, "Schedule deleted successfully.")
        return redirect('admin_schedule_list')
    return render(request, 'sport/admin_confirm_delete.html', {
        'object': schedule,
        'cancel_url': 'admin_schedule_list'
    })

@login_required
@admin_required
def admin_schedule_list_view(request):
    schedules = Schedule.objects.all().order_by('date', 'start_time')
    return render(request, 'sport/schedule_list.html', {
        'schedules': schedules,
        'is_admin_view': True # Flag to indicate admin view
    })



def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'sport/exercise_list.html', {
        'exercises': exercises
    })

@login_required
@admin_required
def admin_exercise_add(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exercise added successfully.")
            return redirect('admin_exercise_list')
    else:
        form = ExerciseForm()
    return render(request, 'sport/exercise_form.html', {'form': form, 'title': 'Add New Exercise'})

@login_required
@admin_required
def admin_exercise_edit(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, "Exercise updated successfully.")
            return redirect('admin_exercise_list')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'sport/exercise_form.html', {'form': form, 'title': f'Edit Exercise: {exercise.name}'})

@login_required
@admin_required
def admin_exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, "Exercise deleted successfully.")
        return redirect('admin_exercise_list')
    return render(request, 'sport/admin_confirm_delete.html', {
        'object': exercise,
        'cancel_url': 'admin_exercise_list'
    })

@login_required
@admin_required
def admin_exercise_list_view(request):
    exercises = Exercise.objects.all()
    return render(request, 'sport/exercise_list.html', {
        'exercises': exercises,
        'is_admin_view': True # Flag to indicate admin view
    })



def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    videos = exercise.videos.all()

    return render(request, 'sport/exercise_detail.html', {
        'exercise': exercise,
        'videos': videos
    })



def blog_list(request):
    posts = BlogPost.objects.select_related('author').all().order_by('-created_at')
    return render(request, 'sport/blog_list.html', {
        'posts': posts
    })

@login_required
@admin_required
def admin_blog_list_view(request):
    posts = BlogPost.objects.select_related('author').all().order_by('-created_at')
    return render(request, 'sport/blog_list.html', {
        'posts': posts,
        'is_admin_view': True # Flag to indicate admin view
    })

@login_required
@admin_required
def admin_blog_add(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Blog post created successfully.")
            return redirect('admin_blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'sport/blog_form.html', {'form': form, 'title': 'Add New Blog Post'})

@login_required
@admin_required
def admin_blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect('admin_blog_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'sport/blog_form.html', {'form': form, 'title': f'Edit Blog Post: {post.title}'})

@login_required
@admin_required
def admin_blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect('admin_blog_list')
    return render(request, 'sport/admin_confirm_delete.html', {
        'object': post,
        'cancel_url': 'admin_blog_list'
    })



def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.select_related('user').all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('content')

            if content:
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    content=content
                )
                messages.success(request, "Comment added successfully.")
                return redirect('blog_detail', pk=pk)
        else:
            messages.error(request, "Login required to comment.")

    return render(request, 'sport/blog_detail.html', {
        'post': post,
        'comments': comments
    })



@login_required
def mark_attendance(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    attendance, created = Attendance.objects.get_or_create(
        student=request.user,
        schedule=schedule,
        date=timezone.now().date()
    )

    if created:
        messages.success(request, "Attendance marked successfully!")
    else:
        messages.info(request, "You already marked attendance today.")

    return redirect('schedule_list')


@login_required
def ai_chat(request):
    response_text = None
    user_input = None
    
    if request.method == "POST":
        user_input = request.POST.get("message")
        try:
            client = genai.Client(api_key=settings.GOOGLE_API_KEY)
            profile = getattr(request.user, 'profile', None)
            
            # Build context for the AI
            context = "You are a professional sport coach."
            if profile:
                training_level = profile.training_level or "Beginner"
                fitness_goal = profile.fitness_goal or "general health and fitness"
                height = f"{profile.height}cm" if profile.height else "unspecified height"
                weight = f"{profile.weight}kg" if profile.weight else "unspecified weight"
                context += f" Advise a {training_level} level athlete. Goal: {fitness_goal}. Height: {height}, Weight: {weight}."

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"{context}\nUser Question: {user_input}"
            )
            response_text = response.text

            # Save to database
            AIConversation.objects.create(
                user=request.user,
                message=user_input,
                response=response_text
            )
        except Exception as e:
            print(f"AI Error: {e}")
            print("--- Debug: Available Gemini Models ---")
            for model in client.models.list():
                print(f"Model Name: {model.name}")
            messages.error(request, "AI service is currently unavailable.")

    # Fetch recent chat history
    history = AIConversation.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    return render(request, 'sport/ai_chat.html', {'response': response_text, 'history': history, 'user_input': user_input})



@login_required
@admin_required
def admin_user_list(request):
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    return render(request, 'sport/admin_user_list.html', {'users': users})

@login_required
@admin_required
def admin_user_add(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('admin_user_list')
    else:
        form = UserRegisterForm()
    return render(request, 'sport/admin_user_form.html', {'form': form, 'title': 'Add New User'})

@login_required
@admin_required
def admin_user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    profile_obj, created = Profile.objects.get_or_create(user=user_obj)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user_obj)
        p_form = ProfileUpdateForm(request.POST, instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "User and Profile updated successfully.")
            return redirect('admin_user_list')
    else:
        u_form = UserUpdateForm(instance=user_obj)
        p_form = ProfileUpdateForm(instance=profile_obj)
    
    return render(request, 'sport/admin_user_form.html', {
        'u_form': u_form,
        'p_form': p_form,
        'title': f'Edit User: {user_obj.username}'
    })

@login_required
@admin_required
def admin_user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('admin_user_list')
        
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('admin_user_list')
    return render(request, 'sport/admin_confirm_delete.html', {
        'object': user_obj,
        'cancel_url': 'admin_user_list'
    })

@login_required
@admin_required
def admin_attendance_list(request):
    attendances = Attendance.objects.select_related('student', 'schedule').all().order_by('-date', '-id')
    return render(request, 'sport/admin_attendance_list.html', {'attendances': attendances})