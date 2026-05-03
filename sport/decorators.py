from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check for profile role OR if user is a staff/superuser
        is_admin = request.user.is_staff or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN')
        if is_admin:
            return view_func(request, *args, **kwargs)
        return redirect('home')
    return wrapper


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'STUDENT' and not request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return redirect('admin_dashboard')
    return wrapper