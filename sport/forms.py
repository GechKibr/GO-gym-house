from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Profile,
    Schedule,
    Exercise,
    SportVideo,
    BlogPost,
    Notification,
    Achievement
)

def add_form_control(fields):
    for field in fields.values():
        if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
            classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{classes} form-control".strip()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    training_level = forms.ChoiceField(
        choices=Profile.TRAINING_LEVEL_CHOICES
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control(self.fields)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                training_level=self.cleaned_data["training_level"],
                role="STUDENT"  # default role
            )
        return user



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control(self.fields)



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "role",
            "age",
            "weight",
            "height",
            "fitness_goal",
            "training_level",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control(self.fields)



class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control(self.fields)



class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "benefits": forms.Textarea(attrs={"rows": 3}),
            "steps": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control(self.fields)



class SportVideoForm(forms.ModelForm):
    class Meta:
        model = SportVideo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control(self.fields)


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "image"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control(self.fields)


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = "__all__"
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }



class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = "__all__"