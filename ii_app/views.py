from django.shortcuts import render, redirect 
from django.shortcuts import HttpResponse
from django.template import loader

from ii_app.forms import RiskForm 
from .models import Project,Employee, Risk, Cone, Booking, Invoice
from .forms import RiskForm


# Create your views here.

def main(request):
    return render (request, 'ii_app/home.html')


def resources(request):
    employee = Employee.objects.all()

    context = {
        'employee': employee,
    }
    return render (request, 'ii_app/resources.html', context)


def resource_detail(request,employee_id):
    resource_detail = Employee.objects.get(pk=employee_id)
    
    context = {
        'resource_detail': resource_detail,

    }
    return render (request, 'ii_app/resource_detail.html', context)

def risk_form(request):
    form = RiskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('')

    return render (request, 'ii_app/risk_form.html', {'form':form})


def update_risk_item(request,risk_id):
    risk = Risk.objects.get(id=risk_id)
    form = RiskForm(request.POST or None,instance = risk)

    if form.is_valid():
        form.save()
        return redirect('')

    return render (request, 'ii_app/risk_form.html', {'form':form, 'risk':risk})


def delete_risk_item(request,risk_id):
    risk = Risk.objects.get(id=risk_id)
  
    if request.method =='POST':
        risk.delete()
        return redirect('')
     
    return render (request, 'ii_app/delete_risk_item.html', {'risk':risk})


def risk_register(request):
    risk_register = Risk.objects.all()

    context = {
        'risk_register': risk_register,
    }
    return render (request, 'ii_app/risk_register.html', context)


def margin(request):
    return render (request, 'ii_app/margin.html')


def finances(request):
    # project_names = Employee.objects.order_by().values('project_name').distinct()
    project_and_employee_names = Employee.objects.order_by('project__code','name').all()
    context = {
        'project_and_employee_names': project_and_employee_names,
    }
    return render (request, 'ii_app/finances.html', context)


def finance_detail (request, code ):
    code = Invoice.objects.filter(project__code = code)

    context = {
        'invoice_values':code
    }
    return render (request, 'ii_app/finance_detail.html', context)
