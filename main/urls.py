from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', include('sport.urls')),
    path('admin/', admin.site.urls),

    path("accounts/login/", auth_views.LoginView.as_view(
        template_name="sport/login.html"
    ), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(
        next_page="/"
    ), name="logout"),
    path('accounts/', include('django.contrib.auth.urls')),
]
