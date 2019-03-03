from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
	path('system/', views.index, name='system'),
    path('', views.SignUp.as_view(), name='signup'),
    path('staff-update/', views.employee_profile_update, name='staff-update'),
    path('<str:id>/staff-image/', views.userImage, name='staff-image-edit'),
    #path('staff-update-hr/', views.employee_profile_admin_update, name='hr-staff-update'),
]
