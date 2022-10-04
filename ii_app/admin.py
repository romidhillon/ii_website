from django.contrib import admin
from .models import Client, Project, Resource, Position, Contract, Assignment, Booking, Invoice, Risk

# Register your models here.
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Resource)
admin.site.register(Position)
admin.site.register(Contract)
admin.site.register(Assignment)
admin.site.register(Booking)
admin.site.register(Invoice)
admin.site.register(Risk)
