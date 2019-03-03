from django import forms

from .models import Training, TrainingApplication, StaffSalary

class TrainingCreationForm(forms.ModelForm):
	class Meta:
		model  = Training
		fields = ['name', 'department', 'training_type', 'description', 'location', 'start_date', 'end_date']

class SalaryCreateForm(forms.ModelForm):
	class Meta:
		model = StaffSalary
		fields = ['staff_name', 'department', 'designation', 'basic_salary', 'tax_rate_apply', 'pension_rate_apply']

# class TrainingApplicationForm(forms.ModelForm):
# 	class Meta:
# 		model  = TrainingApplication
# 		fields = []
# subject = forms.CharField(label='subject', max_length=100 , widget=forms.TextInput(attrs={'class': "form-control"}))