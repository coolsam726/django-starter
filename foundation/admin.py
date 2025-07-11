from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.forms import TextInput
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.resources import ModelResource
from unfold.contrib.import_export.forms import ImportForm, ExportForm, SelectableFieldsExportForm

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from unfold.paginator import InfinitePaginator

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
class TeamAdmin(ModelAdmin, ImportExportModelAdmin):
    # Specify the fields to be displayed in the admin interface
    list_display = ('code', 'name', 'description', 'created_by', 'created_at', 'is_active')
    search_fields = ('code', 'name', 'description')
    list_filter = ('is_active', 'created_by')
    ordering = ('-created_at',)
    # Define the fields to be used in the form
    fields = ('name', 'description', 'is_active')
    paginator = InfinitePaginator
    show_full_result_count = False
    list_per_page = 10
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

class TeamResource(ModelResource):
    description = Field(
        attribute='description',
        column_name='description',
        widget=TextInput,
    )
    class Meta:
        model = Team
        fields = ('id', 'code', 'name', 'description', 'is_active', 'created_at','created_by__username', 'updated_at', 'updated_by__username')
        export_order = ('id', 'code', 'name', 'description', 'is_active', 'created_at', 'created_by__username', 'updated_at', 'updated_by__username'),