from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """사용자 모델의 Admin 페이지를 설정합니다."""
    list_display = ["username", "email", "created_at"]
    list_filter = ["is_staff", "is_superuser", "created_at"]
    search_fields = ["username", "email"]
    ordering = ["-created_at"]
    

