import decimal
from datetime import date
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from company.descriptions import DESIGNATIONS
from employees.models import User
from HR.utils import random_string_generator

# Create your models here.

class Training(models.Model):
	name            = models.CharField(max_length=255)
	department      = models.ForeignKey('employees.Department', on_delete=models.CASCADE)
	training_type   = models.CharField(max_length=255)
	slug            = models.CharField(max_length=255)
	description     = models.TextField()
	location        = models.CharField(max_length=255)
	start_date      = models.DateField(_("Start Date"), default=date.today)
	end_date        = models.DateField(_("End Date"), default=date.today)
	timestamp 		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def unique_slug_generator(self, new_slug=None):
		if new_slug is not None:
			slug = new_slug
		else:
			slug = slugify(self.name)

		Klass = self.__class__
		qs_exists = Klass.objects.filter(slug=slug).exists()
		if qs_exists:
			new_slug = "{slug}-{randstr}".format(
						slug=slug,
						randstr=random_string_generator(size=4)
			        )
			return unique_slug_generator(self, new_slug=new_slug)
		return slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self.unique_slug_generator()
			#print("Slug was sweet..!")
		super().save()

class TrainingApplication(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	training 	= models.ForeignKey(Training, on_delete=models.CASCADE, null=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user, self.training}'

def post_save_training_application_create(sender, instance, created, *args, **kwargs):
	if created:
		TrainingApplication.objects.get_or_create(user=instance)
	training_application, created = TrainingApplication.objects.get_or_create(user=instance)

post_save.connect(post_save_training_application_create, sender=settings.AUTH_USER_MODEL)


class Tax(models.Model):
	name = models.CharField(max_length=200, null=False, blank=False)
	tax_rate = models.DecimalField(decimal_places=2, max_digits=1000)

	def __str__(self):
		return self.name

class Pension(models.Model):
	name = models.CharField(max_length=200, null=False, blank=False)
	pension_rate = models.DecimalField(decimal_places=2, max_digits=1000)

	def __str__(self):
		return self.name

class StaffSalary(models.Model):
	staff_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	department = models.ForeignKey('employees.Department', on_delete=models.CASCADE, null=True)
	designation = models.CharField(max_length=120, choices=DESIGNATIONS)
	basic_salary = models.DecimalField(decimal_places=2, max_digits=100000000)
	tax_rate_apply = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
	tax_apply = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	pension_rate_apply = models.ForeignKey(Pension, on_delete=models.SET_NULL, null=True, blank=True)
	pension_apply = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	wardrobe_allowee = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	health_allowee = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	transport_allowee = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	payable_amount = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)

	def save(self, *args, **kwargs):
		calculate_a = self.basic_salary * decimal.Decimal('0.10') # decimal.Decimal('0.0')
		calculate_b = self.basic_salary * decimal.Decimal('0.10')
		calculate_c = self.basic_salary * decimal.Decimal('0.10')
		
		self.wardrobe_allowee = calculate_a
		self.health_allowee = calculate_b
		self.transport_allowee = calculate_c
		
		if self.tax_rate_apply != None and self.pension_rate_apply != None:
			calculate_d = self.basic_salary * self.tax_rate_apply.tax_rate
			calculate_p = self.basic_salary * self.pension_rate_apply.pension_rate
			self.tax_apply = calculate_d
			self.pension_apply = calculate_p
			self.basic_salary = self.basic_salary - self.tax_apply - self.pension_apply

		elif self.tax_rate_apply == None and self.pension_rate_apply != None:
			#calculate_d = self.basic_salary * self.tax_rate_apply.tax_rate
			calculate_p = self.basic_salary * self.pension_rate_apply.pension_rate
			#self.tax_apply = calculate_d
			self.pension_apply = calculate_p
			self.basic_salary = self.basic_salary - self.pension_apply
		elif self.tax_rate_apply != None and self.pension_rate_apply == None:
			calculate_d = self.basic_salary * self.tax_rate_apply.tax_rate
			self.tax_apply = calculate_d
			self.basic_salary = self.basic_salary - self.tax_apply
		else:
			self.tax_apply = None
			self.pension_apply = None


		all_calculated = calculate_a+calculate_b+calculate_c
		self.basic_salary = self.basic_salary - all_calculated
		self.payable_amount = self.basic_salary + all_calculated

		super(StaffSalary, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('staffwelfare:salary_detail', kwargs={'id': self.id, 'staff': self.staff_name.id})

	def __str__(self):
		return self.staff_name.name

	def get_salary_analysis(self):
		salary_obj = {
                'salary' : self.basic_salary, 
                'allowee1' : self.wardrobe_allowee,
                'allowee2' : self.health_allowee, 'allowee3' : self.transport_allowee,
                'tax' : self.tax_apply or None,
                #'grand_total' : salary + allowee1 + allowee2 + allowee3,
                #'net_total' : grand_total - tax
			}

		return salary_obj
	def get_payable_salary(self):
		all_salary = self.basic_salary+self.wardrobe_allowee+self.health_allowee+self.transport_allowee
		total_salary = all_salary - self.tax_apply
		return total_salary
		#### Another Way To do the tax
		"""
   @property
	   def tax(self):
	      # 10% taxes
	      return self.gross_salary * 0.1

	   @property
	   def net_salary(self):
	      return self.gross_salary - self.tax

		"""
PAYMENT_STATUS_CHOICES = (
   
    ('paid', 'Paid'),
    ('pending', 'Pending'),
    ('withheld', 'Withheld'),
)

class Payment(models.Model):
	staff_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	department = models.ForeignKey('employees.Department', on_delete=models.CASCADE, null=True)
	designation = models.CharField(max_length=120, choices=DESIGNATIONS)
	basic_salary = models.DecimalField(decimal_places=2, max_digits=100000000)
	#tax_rate_apply = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
	tax_apply = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	pension_apply = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	wardrobe_allowee = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	health_allowee = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	transport_allowee = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	payable_amount = models.DecimalField(decimal_places=2, max_digits=100000000, null=True, blank=True)
	status = models.CharField(max_length=100, default='pending', choices=PAYMENT_STATUS_CHOICES)
	payment_date = models.DateField(default=date.today)

	def __str__(self):
		return self.staff_name.name

	def get_absolute_url(self):
		return reverse('staffwelfare:make-payment', kwargs={'id': self.id, 'staff': self.staff_name.id})

class Loan(models.Model):
	staff_name     = models.CharField(max_length=200)
	department     = models.ForeignKey('employees.Department', on_delete=models.CASCADE)
	amount         = models.DecimalField(decimal_places=2, max_digits=100000000)
	reason         = models.CharField(max_length=255)
	active         = models.BooleanField(default=True)
	date           = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.staff_name

class Leave(models.Model):
	staff_name    = models.CharField(max_length=255)
	purpose       = models.CharField(max_length=225)
	slug          = models.CharField(max_length=255)
	start_date    = models.DateField()
	end_date      = models.DateField()
	active        = models.BooleanField(default=True)
	date          = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.name, self.start_date}'

