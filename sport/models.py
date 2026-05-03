from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    TRAINING_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    bio=models.TextField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(help_text="Weight in KG",null=True,blank=True)
    height = models.FloatField(help_text="Height in CM",null=True, blank=True)
    fitness_goal = models.CharField(max_length=255, null=True, blank=True)
    training_level = models.CharField(max_length=20, choices=TRAINING_LEVEL_CHOICES)
    joined_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username



class Schedule(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    focus_area = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.day}"





class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('Cardio', 'Cardio'),
        ('Strength', 'Strength'),
        ('Flexibility', 'Flexibility'),
        ('Breathing', 'Breathing'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    benefits = models.TextField()
    steps = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    difficulty_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class SportVideo(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="videos")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.username} - {self.date}"




class AIConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat with {self.user.username} at {self.created_at}"





class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"



class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    bmi = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.recorded_date}"



class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to="badges/", blank=True, null=True)

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"        

