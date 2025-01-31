from django.contrib import admin
from userauths.models import User, Profile


# Custom admin model for the User model to manage its display in the admin panel
# class UserAdmin(admin.ModelAdmin):
# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['full_name', 'username']
#     list_display = ['username', 'full_name', 'email', 'phone', 'gender']


# Custom admin model for the Profile model to manage its display in the admin panel
# class ProfileAdmin(admin.ModelAdmin):
#     search_fields = ['user__username', 'full_name']
#     list_display = ['thumbnail', 'user', 'full_name', 'verified']


# Register the custom UserAdmin and ProfileAdmin models with the admin site
# This enable the custom display and search functionality for the User and Profile models in the admin panel
# admin.site.register(User, UserAdmin)
# admin.site.register(Profile, ProfileAdmin)
