from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from employees.models import EmployeeProfile, EmployeeProfileTemp, ProfileImage, Guarantor

User = get_user_model()

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfileTemp
        fields = ('user', 'full_name', 'department', 'designation', 'address', 'phone', 'bank_name', 'bank_acc',)

class AdminEmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ('full_name', 'department', 'designation', 'phone', 'staff_type', 'address', 'files', 'bank_name', 'bank_acc',)

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    #widgets = {'password': forms.HiddenInput()}

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'active', 'admin',)
        #widgets = {'password': forms.HiddenInput()}

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ('owner', 'avatar')

class GuarantorCreationForm(forms.ModelForm):
    class Meta:
        model = Guarantor
        exclude = ['timestamp']




