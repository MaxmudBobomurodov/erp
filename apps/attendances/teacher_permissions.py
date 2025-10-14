from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    """
    Faqat teacher foydalanuvchi attendance qo‘sha oladi.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher')
