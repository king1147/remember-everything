from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'login', 'email']
    list_filter = ['id', 'login', 'email']
    readonly_fields = ['id']