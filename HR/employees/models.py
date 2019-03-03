import uuid
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)
from HR.utils import random_string_generator, unique_key_generator
from company.descriptions import STAFF_TYPE
from django.db.models.signals import post_save
from django.dispatch import receiver
from company.descriptions import DESIGNATIONS
from company.models import CompanyProfile
#from staffwelfare import models stf
#from production import models as production_models
from PIL import Image
from simple_history.models import HistoricalRecords
#send_mail(subject, message, from_email, recipient_list, html_message)
def autoKey():
	sample = uuid.uuid4()
	key = hex(int(sample.time_low))[1:]
	return key

def upload_path(instance, filename):
	tx = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), tx)
	#return "images/%s/%s" % (instance.id, filename)
	return 'images/users/{0}/{1}'.format(instance.user.id, filename)

def upload_path_p(instance, filename):
	tx = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), tx)
	#return "images/%s/%s" % (instance.id, filename)
	return 'images/users/{0}/{1}'.format(instance.owner.id, filename)


def upload_file_path(instance, filename):
	new_filename = random.randint(1,3910209312)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "files/{new_filename}/{final_filename}".format(
			new_filename=new_filename, 
			final_filename=final_filename
			)

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.set_password(password) # change user password
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, password=None):
		user = self.create_user(
				email,
				password=password,
				is_staff=True
		)
		return user

	def create_superuser(self, email, password=None):
		user = self.create_user(
				email,
				password=password,
				is_staff=True,
				is_admin=True
		)
		return user

class Department(models.Model):
	name = models.CharField(max_length=100, blank=False, null=False)
	description = models.CharField(max_length=100, blank=True, null=True)
	staff = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.name

class User(AbstractBaseUser):
	email       = models.EmailField(max_length=255, unique=True)
	name 		= models.CharField(max_length=255)
	is_company  = models.BooleanField(default=False)
	active      = models.BooleanField(default=True) # can login 
	staff       = models.BooleanField(default=False) # staff user non superuser
	admin       = models.BooleanField(default=False) # superuser 
	timestamp   = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email' #username
	# USERNAME_FIELD and password are required by default
	REQUIRED_FIELDS = [] #['full_name'] #python manage.py createsuperuser

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_short_name(self):
		if self.name:
			return self.name
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		if self.is_admin:
			return True
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active

class EmployeeProfile(models.Model):
	user 		 = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
	department 	 = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
	full_name    = models.CharField(max_length=255, blank=True, null=True)
	gender 		 = models.CharField(max_length=10)
	address 	 = models.CharField(max_length=255)
	phone 		 = models.CharField(max_length=255)
	files 		 = models.FileField(upload_to=upload_file_path, null=True, blank=True)
	bank_name 	 = models.CharField(max_length=150)
	bank_acc 	 = models.CharField(max_length=150)
	designation  = models.CharField(max_length=120, choices=DESIGNATIONS)
	staff_type   = models.CharField(max_length=120, choices=STAFF_TYPE)
	training 	 = models.ManyToManyField('staffwelfare.Training', blank=True) # publications = models.ManyToManyField(Publication)
	appraisals 	 = models.PositiveIntegerField(default=0)
	displinary 	 = models.PositiveIntegerField(default=0)
	staff_key 	 = models.CharField(max_length = 100, default=autoKey())
	employee_temp_profil = models.ForeignKey('EmployeeProfileTemp', on_delete=models.CASCADE, null=True)
	history 	 = HistoricalRecords()

	def __str__(self):
		return f'{self.user.email}'

	def get_absolute_url(self):
		return reverse('employee:staff_detail', kwargs={'id': self.id, 'staff_key': self.staff_key})

	def get_account_detail(self):
		return "{ful_name}\n{bank}\n{account}, {staff_num}".format(
		ful_name  = self.full_name or "",
		bank      = self.bank_name,
		account   = self.bank_acc,
		staff_num = self.staff_key
		)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	if instance.is_company:
		CompanyProfile.objects.get_or_create(user = instance)
	else:
		EmployeeProfile.objects.get_or_create(user = instance)
	
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	print('_-----')
	# print(instance.internprofile.bio, instance.internprofile.location) 
	if instance.is_company:
		instance.company_profile.save()
	else:
		EmployeeProfile.objects.get_or_create(user = instance)

class Guarantor(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	full_name 	= models.CharField(max_length=100, blank=False, null=False)
	email 		= models.EmailField(max_length=100, blank=False, null=False)
	image 		= models.ImageField(upload_to=upload_path)
	address 	= models.TextField()
	occupation  = models.CharField(max_length=255, blank=True, null=True)
	designation = models.CharField(max_length=200, blank=True, null=True)
	years_known = models.CharField(max_length=200)
	phone 		= models.CharField(max_length=200, blank=False, null=False, help_text="phone1, phone2,,,")
	timestamp 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		#return f'{self.user.email, self.full_name}'
		return self.user.email

	def get_absolute_url(self):
		return reverse('employee:staff_detail', kwargs={'id': self.user.id, 'email': self.email})


class EmployeeProfileTemp(models.Model):
	#user 		 = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='employee_temp_profile')
	user 	 	 = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='employee_temp_profile')
	department 	 = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
	full_name    = models.CharField(max_length=255, blank=True, null=True)
	gender 		 = models.CharField(max_length=10)
	address 	 = models.CharField(max_length=255)
	phone 		 = models.CharField(max_length=255)
	#avatar		 = models.ImageField(upload_to=upload_path, default='default.png', null=True, blank=True)
	files 		 = models.FileField(upload_to=upload_file_path, null=True, blank=True)
	bank_name 	 = models.CharField(max_length=150)
	bank_acc 	 = models.CharField(max_length=150)
	designation  = models.CharField(max_length=120, choices=DESIGNATIONS)
	staff_type   = models.CharField(max_length=120, choices=STAFF_TYPE)
	training 	 = models.ManyToManyField('staffwelfare.Training', blank=True) # publications = models.ManyToManyField(Publication)
	appraisals 	 = models.PositiveIntegerField(default=0)
	displinary 	 = models.PositiveIntegerField(default=0)
	pending		 = models.BooleanField(default=True)
	timestamp	 = models.DateTimeField(auto_now_add=True)
	history 	 = HistoricalRecords()

	def __str__(self):
		return f'{self.user}'

	def get_absolute_url(self):
		return reverse('employee:staff_detail_ad', kwargs={'id': self.id, 'full_name': self.full_name})

class ProfileImage(models.Model):
	owner 	= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_image') 
	avatar  = models.ImageField(upload_to=upload_path_p, default='default.png')

	def __str__(self):
		return self.owner.name #user

	def get_absolute_url(self):
		return reverse('company:staff-image-edit', kwargs={'id': self.owner.id})

	def save(self, **kwargs):
		super().save()

		img = Image.open(self.avatar.path)
		if img.height > 400 or img.width > 400:
			output_size = (400, 400)
			img.thumbnail(output_size)
			img.save(self.avatar.path)

