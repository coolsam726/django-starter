from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

from foundation.models import Team

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(ModelAdmin):
    # Specify the fields to be displayed in the admin interface
    list_display = ('code', 'name', 'description', 'created_by', 'created_at', 'is_active')
    search_fields = ('code', 'name', 'description')
    list_filter = ('is_active', 'created_by')
    ordering = ('-created_at',)
    # Define the fields to be used in the form
    fields = ('name', 'description', 'is_active')