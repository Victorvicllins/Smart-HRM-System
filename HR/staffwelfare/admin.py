from django.contrib import admin
from .models import Training, TrainingApplication, StaffSalary, Tax, Pension, Payment
# Register your models here.

admin.site.register(Training)
admin.site.register(TrainingApplication)
admin.site.register(StaffSalary)
admin.site.register(Tax)
admin.site.register(Payment)
admin.site.register(Pension)

