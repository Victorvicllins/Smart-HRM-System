from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from simple_history.admin import SimpleHistoryAdmin
from employees.models import Department, EmployeeProfile, EmployeeProfileTemp
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import CompanyProfile

# Register your models here.
admin.site.site_header = "Pandas Administration"
User =get_user_model()

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    class Meta:
        model = Department
admin.site.register(Department, DepartmentAdmin)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_company',)
    list_filter = ('admin', 'is_company', 'active')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password',)}),
        ('Personal Info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'is_company', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'name', )
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
# Company Profiles
# class CompanyProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'full_name', 'address',)
#     search_fields = ['full_name', 'city', 'address']
#     class Meta:
#         model = CompanyProfile
# admin.site.register(CompanyProfile, CompanyProfileAdmin)
#admin.site.register(SimpleHistoryAdmin)

class CompanyProfileHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["user", "full_name", "shortname"]
    history_list_display = ["shortname"]
    search_fields = ['full_name', 'user__full_name']
admin.site.register(CompanyProfile, CompanyProfileHistoryAdmin)

# Employees Profiles
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone',)
    search_fields = ['full_name', 'department', 'address']
    class Meta:
        model = EmployeeProfile
admin.site.register(EmployeeProfile, EmployeeProfileAdmin)

admin.site.register(EmployeeProfileTemp)