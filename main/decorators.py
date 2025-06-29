from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.contrib.auth.models import User
from .models import Teacher

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Необходимо войти в систему')
            return redirect('login')
        
        if not request.user.is_staff:
            messages.error(request, 'Доступ запрещен. Необходимы права администратора')
            return redirect('document_list')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Необходимо войти в систему')
            return redirect('login')
        
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            if not request.user.is_staff:
                messages.error(request, 'Доступ запрещен. Необходим статус преподавателя')
                return redirect('login')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view 