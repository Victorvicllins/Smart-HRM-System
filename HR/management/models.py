import os
import random
import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from company.descriptions import DESIGNATIONS
from employees.models import User
from HR.validators import validate_extension
# Create your models here.
#User = get_user_model()

def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_path(instance, filename):
	tx = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), tx)
	#return "images/%s/%s" % (instance.id, filename)
	return 'images/users/{0}/{1}'.format(instance.id, filename)

def upload_file_path(instance, filename):
	new_filename = random.randint(1,3910209312)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "files/{new_filename}/{final_filename}".format(
			new_filename=new_filename, 
			final_filename=final_filename
			)		
def upload_task_file_path(instance, filename):
	new_filename = random.randint(1,3910209312)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "tasks/{new_filename}/{final_filename}".format(
			new_filename=new_filename, 
			final_filename=final_filename
			) 
	# ManyToManyField

class Report(models.Model):
	report_by 	= models.CharField(max_length=200, blank=False, null=False)
	#user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title 		= models.CharField(max_length=200, blank=False, null=False)
	slug 		= models.SlugField(max_length=255, unique=True)
	content 	= models.TextField(blank=False, null=False)
	files 		= models.FileField(upload_to=upload_file_path, blank=True, null=True, validators=[validate_extension])
	updated 	= models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp 	= models.DateTimeField(auto_now=False, auto_now_add=True)
# instance
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("management:detail", kwargs={"id": self.id, "slug": self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]

	def clean(self, *args, **kwargs):
		if self.title == '':
			raise ValidationError('Report subject cannot be empty') #instance
		super(Report, self).clean(*args, **kwargs)

	def _get_unique_slug(self):
		slug = slugify(self.title)
		unique_slug = slug
		num = 1
		while Report.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super().save()

class Penalty(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	staff_name = models.CharField(max_length=255)
	description = models.CharField(max_length=100, blank=False, null=False)
	start_date = models.DateField()
	end_date = models.DateField()
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user
#PositiveIntegerField ManyToManyField(Publication)

class Task(models.Model):
	#tasker 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	#tasker		= models.ManyToManyField(User)
	tasker		= models.CharField(max_length=255, blank=False, null=False)
	staff_name 	= models.CharField(max_length=255)
	title 		= models.CharField(max_length=255, blank=False, null=False)
	description = models.TextField(blank=True, null=True)
	start_date 	= models.DateField()
	end_date 	= models.DateField()
	file 		= models.FileField(upload_to=upload_task_file_path, validators=[validate_extension])
	active		= models.BooleanField(default=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("management:task-detail", kwargs={"id": self.id})


