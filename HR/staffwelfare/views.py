import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import View
from django.utils import timezone
from django.template.loader import get_template
from HR.utils import random_string_generator, render_to_pdf
from employees.models import ProfileImage
from .forms import TrainingCreationForm, SalaryCreateForm
from .models import Training, StaffSalary, Payment
# Create your views here.

def training(request):
	image = ProfileImage.objects.filter(owner=request.user)
	if request.method == "POST":
		form = TrainingCreationForm(request.POST)
		if form.is_valid():
			form.save()
			print("Yesss got form data.")
			return redirect('company:system')
	else:
		form = TrainingCreationForm()
		context = {
			'image': image,
			'form': form,
			}
	return render(request, 'joli/form-layouts-two-column.html', context)

def staffsalary(request):
	image = ProfileImage.objects.filter(owner=request.user)
	if request.method == 'POST':
		form = SalaryCreateForm(request.POST)
		if form.is_valid():
			form.save()
			print("Yesss i got form data.")
			return redirect('company:system')
	else:
		form = SalaryCreateForm()
		context = {
			'image': image,
			'form': form
		}
	return render(request, 'joli/form-validation.html', context)

def staffsalarylist(request):
	salary = StaffSalary.objects.all()
	image = ProfileImage.objects.filter(owner=request.user)
	#total = StaffSalary.get_payable_salary(staff_name='test@test.com')
	#print(total)

	context = {
		'image': image,
		'all_salary': salary,
	}
	return render(request, 'joli/account/table-basic.html', context)

def make_payent(request, id=None, staff=None, *args, **kwargs):
	pay_staff = get_object_or_404(StaffSalary, id=id, staff_name_id=staff)
	try:
		staff_payment = Payment.objects.create(
				staff_name          = pay_staff.staff_name,
				department          = pay_staff.department,
				designation         = pay_staff.designation,
				basic_salary        = pay_staff.basic_salary,
				tax_apply           = pay_staff.tax_apply,
				pension_apply       = pay_staff.pension_apply,
				wardrobe_allowee    = pay_staff.wardrobe_allowee,
				health_allowee      = pay_staff.health_allowee,
				transport_allowee   = pay_staff.transport_allowee,
				payable_amount      = pay_staff.payable_amount,
				status              = "paid"
								)
		if staff_payment:
			print("Weldone sir..!!")
			return HttpResponseRedirect('staffwelfare:payment_list')
	except Exception as e:
		print(e)
	return render(request, 'joli/table-export.html')

def make_payment_view(request, id=None, staff=None, *args, **kwargs):
	# fiter by search months or get all
	payments = query_set = get_object_or_404(StaffSalary, id=id, staff_name_id=staff)
	image = ProfileImage.objects.filter(owner=request.user)
	context = {
		"image": image,
		"payments": payments,
	}
	return render(request, 'joli/account/payment.html', context)

class GeneratePaymentPdf(View):
	def get(self, request, id=None, staff=None, *args, **kwargs):
		today = timezone.now().date()
		query_set = get_object_or_404(Payment, id=id, staff_name_id=staff)
		template = get_template("pdf/account/payment/report_pdf.html")
		
		context = {
			"query_set": query_set,
			"today": today,
		}
		#var = template.render(context)
		pdf = render_to_pdf("pdf/account/payment/report_pdf.html", context)
		if pdf:
			respone = HttpResponse(pdf, content_type='application/pdf')
			size = random.randint(10, 45)
			key = random_string_generator(size=size)
			#filename = "%s.pdf" % (query_set.report_by+key)
			name = query_set.staff_name.name.replace(' ', '_')
			filename = "payslip_%s.%s.pdf" % (name,key[:7])
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get('download')
			if download:
				content = "attachment; filename='%s'" %(filename)
			respone["Content-Disposition"] = content
			return respone
		return HttpResponse("No file found.")

def payment_view(request):
	# fiter by search months or get all
	payments = Payment.objects.all()
	image = ProfileImage.objects.filter(owner=request.user)
	#print("This is ", payments)

	context = {
		"payments": payments,
		"image": image,
	}
	return render(request, 'joli/table-export.html', context)

class GeneratePdf(View):
	def get(self, request, id=None, staff=None, *args, **kwargs):
		today = timezone.now().date()
		query_set = get_object_or_404(StaffSalary, id=id, staff_name_id=staff)
		template = get_template("pdf/account/report_pdf.html")
		
		context = {
			"query_set": query_set,
			"today": today,
		}
		#var = template.render(context)
		pdf = render_to_pdf("pdf/account/report_pdf.html", context)
		if pdf:
			respone = HttpResponse(pdf, content_type='application/pdf')
			size = random.randint(10, 45)
			key = random_string_generator(size=size)
			#filename = "%s.pdf" % (query_set.report_by+key)
			filename = "salary_%s.%s.pdf" % (query_set.staff_name,key[:11])
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get('download')
			if download:
				content = "attachment; filename='%s'" %(filename)
			respone["Content-Disposition"] = content
			return respone
		return HttpResponse("No file found.")

class TrainingList(generic.ListView):
	template_name = 'joli/table-basic2.html'
	def get_queryset(self):
		now = timezone.now()
		training = Training.objects.all()
		upcoming = Training.objects.filter(start_date__gte=now).order_by('start_date')
		passed = Training.objects.filter(start_date__lt=now).order_by('-start_date')
		print(upcoming)
		# print(training)
		print(passed)
		#queryset = list(upcoming) + list(passed)
		return upcoming
		
		#def get_context_data(self, **kwargs):
		#	context = super(TrainingList, self).get_context_data(**kwargs)

