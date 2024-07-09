"""
CustomUserModel admin zone registration
"""
from django.contrib import admin

from .models import CustomUser

admin.site.register(CustomUser)
