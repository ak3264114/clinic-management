from django.contrib import admin

from management.models import Appointment, Doctor, Patient


# Register your models here
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
