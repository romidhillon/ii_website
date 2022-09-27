from django.contrib import admin
from .models import Project, Employee, Risk, Cone, Booking, Invoice

# Register your models here.
admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(Risk)
admin.site.register(Cone)
admin.site.register(Booking)
admin.site.register(Invoice)
