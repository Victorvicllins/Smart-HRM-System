from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from company.decorators import company_required
from employees.models import EmployeeProfile, Guarantor, ProfileImage
from management.models import Task
from employees.forms import GuarantorCreationForm

# For all employees
@login_required
def employee(request):
	today = timezone.now().date()
	personal_image = ProfileImage.objects.filter(owner=request.user)
	image = ProfileImage.objects.all()
	queryset_list = EmployeeProfile.objects.all()
	paginator = Paginator(queryset_list, 8)
	page = request.GET.get('page')
	queryset_list = paginator.get_page(page)

	### For staff search

	query = request.GET.get("q")
	if query:
		queryset_list = EmployeeProfile.objects.filter(Q(user__email__icontains=query)|
									Q(full_name__icontains=query)|
									Q(address__icontains=query)|
									Q(gender__icontains=query)|
									Q(phone__icontains=query)|
									Q(staff_key__icontains=query)
								).distinct()

	context = {
		'employee_list': queryset_list,
		'personal_image': personal_image,
		'image': image,
	}
	return render(request, 'joli/pages-address-book.html', context)
## product = get_object_or_404(Product, id=id, slug=slug, available=True)

def employeeDetail(request, id, staff_key):
	profile = get_object_or_404(EmployeeProfile, id=id, staff_key=staff_key)
	image = ProfileImage.objects.filter(owner=request.user)
	context = {
		'image': image,
		'profile': profile,
	}
	return render(request, 'joli/pages-profile.html', context)

def taskDetail(request, id):
	task = get_object_or_404(Task, id=id)
	image = ProfileImage.objects.filter(owner=request.user)
	context = {
		'task': task,
		'image': image,
	}
	return render(request, 'joli/pages2-profile.html', context)

@login_required
@company_required
def taskList(request):
	today = timezone.now().date()
	task_list = Task.objects.all()
	competed_task = Task.objects.filter(end_date__lt=today)
	
	image = ProfileImage.objects.filter(owner=request.user)
	### For staff search
	query = request.GET.get("q")
	if query:
		task_list = task_list.filter(Q(title__icontains=query)|
									Q(description__icontains=query)
								).distinct()

	context = {
		'image': image,
		'task_list': task_list,
		'competed_task': competed_task,
	}
	return render(request, 'joli/pages-tasks.html', context)

def taskCreation(request):
	profiles = EmployeeProfile.objects.all()
	image = ProfileImage.objects.filter(owner=request.user)
	if request.method == 'POST':
		user = request.user
		staff = request.POST.get('staff')
		title = request.POST.get('title')
		stdate = request.POST.get('stdate')
		dudate = request.POST.get('dudate')
		description = request.POST.get('description')
		file = request.FILES.get('filename', None)
		try:
			task_ = Task.objects.create(tasker=user, staff_name=staff, title=title, 
								description=description, start_date=stdate,
								end_date=dudate, file=file)
			print("Task created successfully.")
			#return HttpResponseRedirect('company:system')
		except Exception as e:
			print(e)

		#print(user, staff, stdate, description, file)
	context = {
		'image': image,
		'profiles': profiles,
	}
	return render(request, 'joli/form-layouts-one-column.html', context)

def staffguarantor(request):
	guarantor = Guarantor.objects.filter(user=request.user)
	image = ProfileImage.objects.filter(owner=request.user)
	if request.method == 'POST' and request.FILES['image']:
		form = GuarantorCreationForm(request.POST, request.FILES)
		if form.is_valid():
			done = form.save()
			if done:
				print("Yes done..!")
			print('Guarantor created for ', request.user)
			return redirect('employee:guarantor')
	else:
		print(guarantor)
		form = GuarantorCreationForm()

	context = {
			'guarantors': guarantor,
			'form': form,
			'image': image,

		}

	return render(request, 'joli/ui-widgets.html', context)
