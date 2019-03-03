from django.contrib import admin
from django.urls import path
from employees.views import taskDetail
from . import views

app_name = "management"

urlpatterns = [
    path('reports/', views.post_list, name='list'),
    path('create/', views.post_create, name="make-report"),
    path('<int:id>/<str:slug>/', views.post_detail, name="detail"),
    path('task/<int:id>/', taskDetail, name="task-detail"),
    #path('<int:id>/edit/', views.post_update, name="update"),
    #path('<int:id>/delete/', views.post_delete, name="delete"),
    path('<int:id>/<str:slug>/pdf/', views.GeneratePdf.as_view(), name='for-pdf'),
    path('compose-mail/', views.mailer, name="compose-mail"),
]
