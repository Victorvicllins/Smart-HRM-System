import random
from urllib.parse import quote 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from django.views.generic import View
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from company.descriptions import DESIGNATIONS
from HR.utils import random_string_generator, render_to_pdf
from employees.models import ProfileImage
from .models import Report
from .forms import PostForm

# Register your models here.

User = get_user_model()
# Create your views here. instance

def post_create(request):
	#if not request.user.is_staff or not request.user.is_superuser:
	#	raise Http404NA
	designations = DESIGNATIONS
	image = ProfileImage.objects.filter(owner=request.user)
	if request.method == "POST":
		user = request.user
		subject = request.POST.get('title')
		#designation = request.POST.get('designation')
		content = request.POST.get('content')
		
		file = request.FILES['file']
		
		try:
			print("Yeess i got form data from try.")
			Report.objects.create(
						report_by=user,
						title=subject,
						content=content,
						files=file)
			messages.success(request, "Successfully Created.!")
			print("Yeess.! That was a great one.")
			return HttpResponseRedirect(instance.get_absolute_url())
		except Exception as e:
			print(e)
	context = {
		'image': image,
		"designations": designations,
	}
	return render(request, "joli/form-editors.html", context)

def post_detail(request, id=None, slug=None):
	instance = get_object_or_404(Report, id=id, slug=slug)
	image = ProfileImage.objects.filter(owner=request.user)
	share_string = quote(instance.content)
	context = {
		"instance": instance,
		"title": instance.title,
		"share_string": share_string,
		"image": image,
		}
	if not request.user.is_company:
		return render(request, "joli/pages-timeline-simple.html", context)
	else:
		return render(request, "joli/admin/pages-timeline-simple.html", context)

# # For the Home Page..!

def post_list(request):
	if not request.user.is_company:
		user = request.user
		all_report = Report.objects.filter(report_by=user)
		image = ProfileImage.objects.filter(owner=user)
		print(user)
		context = {
			"all_report": all_report,
			"image": image,
		}

		return render(request, "joli/pages-messages.html", context)
	else:
		user = request.user
		all_report = Report.objects.all()
		image = ProfileImage.objects.filter(owner=user)
# 	featured = Report.objects.filter(category="LATEST")
# 	paginator = Paginator(all_post, 5)
# 	page = request.GET.get('page')
# 	contacts = paginator.get_page(page)

# 	all_gist_post = Report.objects.filter(category="GISTS")
# 	all_event_post = Report.objects.filter(category="EVENTS")
# 	all_celeb_post = Report.objects.filter(category="CELEBS")
# 	all_politics_post = Report.objects.filter(category="POLITICS")


		context = {
			"all_report": all_report,
			"image": image,
		}

		return render(request, "joli/admin/pages-messages.html", context)

# def post_update(request, id=None):
# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404
# 	instance = get_object_or_404(Report, id=id)
# 	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		messages.success(request, "Successfully Edited.!")
# 		return HttpResponseRedirect(instance.get_absolute_url())

# 	context = {
# 		"instance": instance,
# 		"title": instance.title,
# 		"form": form,
# 		}
# 	return render(request, "blog/post_create.html", context)

# def post_delete(request, id=None):
# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404
# 	instance = get_object_or_404(Report, id=id)
# 	instance.delete()
# 	messages.success(request, "Article Successfully Deleted.!")
# 	return redirect("myblog:list")

# The pdf generator
class GeneratePdf(View):
	def get(self, request, id=None, slug=None, *args, **kwargs):
		today = timezone.now().date()
		query_set = get_object_or_404(Report, id=id, slug=slug)
		template = get_template("pdf/report_pdf.html")
		context = {
			"query_set": query_set,
			"today": today,
		}
		#var = template.render(context)
		pdf = render_to_pdf("pdf/report_pdf.html", context)
		if pdf:
			respone = HttpResponse(pdf, content_type='application/pdf')
			size = random.randint(10, 45)
			key = random_string_generator(size=size)
			filename = "%s.pdf" % (query_set.report_by+key)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get('download')
			if download:
				content = "attachment; filename='%s'" %(filename)
			respone["Content-Disposition"] = content
			return respone
		return HttpResponse("No file found.")

def mailer(request):
	user = request.user
	image = ProfileImage.objects.filter(owner=user)
	message = "i love programming."
	send_mail("Testing to Django.",
				message,
				settings.EMAIL_HOST_USER,
				['vicllins@gmail.com'], fail_silently=False)

	context = {
		"image": image,
	}
	return render(request, 'joli/pages-mailbox-compose.html', context)
