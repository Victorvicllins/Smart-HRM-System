# Welfare urls
from django.urls import path
from .views import training, TrainingList, staffsalary, staffsalarylist, GeneratePdf, payment_view, make_payent, GeneratePaymentPdf, make_payment_view

app_name = "staffwelfare"

urlpatterns = [
	path('', training, name="training"),
	path('all-training/', TrainingList.as_view(), name="all-training"),
	path('staff/', staffsalary, name='staff_salary'),
	path('staff-list/', staffsalarylist, name='salary-list'),
	path('salary-detail/<int:id>/<str:staff>', GeneratePdf.as_view(), name='salary_detail'),
	path('staff-payments/', payment_view, name="payment_list"),

	path('payment/<int:id>/<str:staff>/', make_payment_view, name="make-payment"), # Salary detatil
	path('pay-staff/<int:id>/<str:staff>/', make_payent, name="payment"), # Create payment action
	path('payment_pdf/<int:id>/<str:staff>/pdf/', GeneratePaymentPdf.as_view(), name='payment_pdf'), # Pay slip
]

