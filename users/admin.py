from django.contrib import admin
from django.apps import apps
from users.models import Users

UsersModel = apps.get_model('users', 'Users')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'full_name', 'username', 'email', 'gender', 'role',  'contact', 'address', 'created_at']
    search_fields = ['full_name', 'username', 'email', 'address', 'contact']
    list_filter = ['role', 'gender']
    list_per_page = 15
