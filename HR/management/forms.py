# Form to create report
from django import forms
from .models import Report

class PostForm(forms.ModelForm):
	class Meta():
		model = Report
		fields = [
				"title",
				"files",
			]

