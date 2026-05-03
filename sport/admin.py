from django.contrib import admin
from .models import (
    Profile,
    Schedule,
    Exercise,
    SportVideo,
    Attendance,
    AIConversation,
    BlogPost,
    Comment,
    Notification,
    Progress,
    Achievement,
    UserAchievement,
)



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'weight', 'height', 'training_level', 'joined_date')
    list_filter = ('training_level', 'joined_date')
    search_fields = ('user__username', 'fitness_goal')
    ordering = ('-joined_date',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'day', 'date', 'start_time', 'duration_minutes', 'focus_area')
    list_filter = ('day', 'focus_area', 'date')
    search_fields = ('title', 'focus_area')
    ordering = ('date',)    



class SportVideoInline(admin.TabularInline):
    model = SportVideo
    extra = 1


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'duration_minutes', 'difficulty_level', 'created_at')
    list_filter = ('category', 'difficulty_level')
    search_fields = ('name', 'category')
    inlines = [SportVideoInline]


@admin.register(SportVideo)
class SportVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'exercise', 'added_at')
    search_fields = ('title',)
    list_filter = ('added_at',)    




@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'schedule', 'date', 'present')
    list_filter = ('date', 'present')
    search_fields = ('student__username',)


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'content', 'created_at')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'bmi', 'recorded_date')
    list_filter = ('recorded_date',)
    search_fields = ('user__username',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_date')
    list_filter = ('earned_date',)
    search_fields = ('user__username', 'achievement__name')






admin.site.site_header = "GO-SIKED System"
admin.site.site_title = "Sport Admin"
admin.site.index_title = "Welcome to GO-SIKED Sport Dashboard"