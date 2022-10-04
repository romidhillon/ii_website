from django.shortcuts import render, redirect 
from django.shortcuts import HttpResponse
from django.template import loader
from django.db.models import Sum

from ii_app.forms import RiskForm 
from .models import Project, Resource, Position, Contract, Assignment,  Booking, Invoice, Risk
from .forms import RiskForm


# Create your views here.

def main(request):
    return render (request, 'ii_app/home.html')


def resources(request):
    resource = Resource.objects.all()
    assignment = Assignment.objects.all()
    project_and_resource = zip(resource, assignment)
  

    context = {
        'project_and_resources': project_and_resource ,
    }

    return render (request, 'ii_app/resources.html', context)


def resource_detail(request,id,id_2,):
    resource= Resource.objects.get(id = id)
    assignment= Assignment.objects.get(id = id_2)

    context = {
        'resource': resource,
        'assignment': assignment,

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
    project_and_employee_names = Project.objects.order_by('code','title').all()
    context = {
        'project_and_employee_names': project_and_employee_names,
    }
    return render (request, 'ii_app/finances.html', context)


def finance_detail (request, code):
    invoice_values = Invoice.objects.filter(project__code = code)
    # sum_of_invoice_values = Invoice.objects.aggregate(Sum=Sum('value'))['Sum']

    # hours = Booking.objects.values("project__code").annotate(sum=Sum('hours'))[0]['sum']
    # hours = int(hours)

    # charge_rate = Cone.objects.values("employee__project__code").annotate(sum=Sum('rate'))[0]['sum']

    # life_to_date = hours * charge_rate
    
    context = {
        'invoice_values':invoice_values,
        # 'sum_of_invoice_values':sum_of_invoice_values,
        # 'life_to_date':life_to_date,
    }
    return render (request, 'ii_app/finance_detail.html', context)

def cv(request):
    resource = Resource.objects.all()

    context = {
        'resource': resource ,
    }

    return render (request, 'ii_app/cv.html', context)