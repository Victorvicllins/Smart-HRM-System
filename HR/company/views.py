from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from company.forms import UserAdminCreationForm, UserAdminChangeForm, UserUpdateForm
from company.models import CompanyProfile
from employees.models import EmployeeProfile, EmployeeProfileTemp, User, ProfileImage
from employees.forms import EmployeeUpdateForm, AdminEmployeeUpdateForm, ProfileImageForm
from management.models import Report, Task
from staffwelfare.forms import TrainingCreationForm
from staffwelfare.models import Training
#User = get_user_model()

# Create your views here.
class SignUp(CreateView):
	form_class = UserAdminCreationForm
	success_url = reverse_lazy('login')
	template_name = 'index.html'

def index(request):
	today = timezone.now().date()
	if not request.user.is_authenticated:
		raise Http404
	if request.user.is_company:
		r_user = request.user
		user = CompanyProfile.objects.all()
		#profile = user.company_profile.company_url
		employee = EmployeeProfile.objects.all()
		active_trainings = Training.objects.all()
		current_trainings = Training.objects.all()
		completed_trainings = Training.objects.all() #
		image = ProfileImage.objects.filter(owner=r_user)
		context = {
				'today': today,
				'employee': employee,
				'users': user,
				'active_trainings': active_trainings,
				'current_trainings': completed_trainings,
				'completed_trainings': completed_trainings,
				'image': image,
		}
	
		return render(request, 'joli/index.html', context)
	else:
		user = request.user
		user_ = User.objects.get(email=user)
		profile = EmployeeProfile.objects.get(user=user_)
		image = ProfileImage.objects.filter(owner=user)
		tasks = Task.objects.filter(staff_name=user)
		if image == None:
			image = None
		# for img in image:
		# 	print(img.avatar)
		# print('*'*5)
		# print(profile.user)
		# print(user.email)
		context = {
			'profiles': profile,
			'user': user,
			'image':image,
			'tasks': tasks,
			'today': today,
		}
		return render(request, 'joli/pages-profile.html', context)

@login_required
def employee_profile_update(request):
	image = ProfileImage.objects.filter(owner=request.user)
	if request.method == 'POST':
		#user = User.objects.all()
		user_form     = UserUpdateForm(request.POST, instance=request.user)
		profile_form  = EmployeeUpdateForm(request.POST, request.FILES or None,
											instance=request.user.employee_profile.employee_temp_profil)
		
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			print("Yesss i got form data.")
			return redirect('company:system')
	else:
		user_form 	  = UserUpdateForm(instance=request.user)
		profile_form  = EmployeeUpdateForm(instance=request.user.employee_profile.employee_temp_profil)
		
		context = {
		'user_form': user_form,
		'profile_form': profile_form,
		'image': image,
		}
	return render(request, 'joli/form-elements.html', context)

@login_required
def employee_profile_admin_list(request):
	pending = EmployeeProfileTemp.objects.filter(pending=True)
	context = {
		'pending': pending,
	}		
	return render(request, 'joli/table-basic.html', context)

def employee_profile_admin_update(request, id, full_name):
	object_ = get_object_or_404(EmployeeProfileTemp, id=id, full_name=full_name)
	print(object_.user)
	if request.method == "POST":
		user_form     = UserUpdateForm(request.POST, instance=object_.user)
		profile_form  = AdminEmployeeUpdateForm(request.POST, request.FILES or None,
											instance=object_.user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			done = profile_form.save()
			if done:
				object_.delete()
				print("Done.")
			return redirect('company:system')
	else:
		user_form 	  = UserUpdateForm(instance=object_.user)
		profile_form  = AdminEmployeeUpdateForm(instance=object_)
	context = {
			'object': object_,
			'user_form': user_form,
			'profile_form': profile_form,
		}
	return render(request, 'joli/admin/form-elements.html', context)
	
def userImage(request, id):
	image = ProfileImage.objects.filter(id=request.user.id)
	object_ = ProfileImage.objects.filter(owner=request.user)
	if request.method == 'POST' and request.FILES['avatar']:
		form = ProfileImageForm(request.POST, request.FILES)
		object_.delete()
		#print(request.POST.get('owner'))
		#print(request.FILES['avatar'])
		if form.is_valid():
			done = form.save()
			if done:
				print("Profile picture saved for ", request.user)
	else:
		form = ProfileImageForm(instance=request.user)
	context = {
		'image': image,
		'form': form,
	}

	return render(request, 'joli/profile-image.html', context)
