from django.urls import path, re_path
from company.views import employee_profile_admin_list, employee_profile_admin_update
from . import views

app_name = "employee"

urlpatterns = [
    path('staff/', views.employee, name='home'),
    path('task-form/', views.taskCreation, name='task-form'),
    path('task-list/', views.taskList, name='task-list'),
    path('staff/<int:id>/<str:staff_key>/', views.employeeDetail, name='staff_detail'),
    path('staff-update-admin/', employee_profile_admin_list, name='update_list'),
    path('<int:id>/<str:full_name>/edit/', employee_profile_admin_update, name='staff_detail_ad'),
    path('guarantor/', views.staffguarantor, name='guarantor'),
    #re_path(r'^(?P<id>\d+)/(?P<staff_key>[-\w]+)/$', views.employeeDetail, name='staff_detail'),
]

# url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
 #path('articles/<slug:title>/<int:section>/', views.section, name='article-section'),