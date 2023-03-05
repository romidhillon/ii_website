from calendar import c
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, Q, Count
from django.db.models.functions import Coalesce
from datetime import date, timedelta

from django.urls import reverse

from ii_app.forms import RiskForm, BookingForm
from .models import Project, Resource, Assignment, Booking, Risk
from .forms import RiskForm, BookingForm
import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .serializers import ProjectSerializer
from django.template.defaulttags import register
from rest_framework.decorators import api_view 
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

@register.filter
def get_value(d,k):
    return d.get(k)

@login_required(login_url='sign_in')
def main(request):
    week_start = date.today()
    week_start -= timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=4)

    period_end = datetime.date.today().replace(day=1)
    period_start = (period_end - datetime.timedelta(days=1)).replace(day=1)

    live_projects = Assignment.objects.filter(
        start__lte=week_start,
        end__gt=week_end
    ).values('position__project__code').annotate(sum=Count('position'))
    live_projects = [
        (project['position__project__code'], project['sum'])
        for project in live_projects
    ]

    assignment_hours = Booking.objects.filter(
        day__gte=week_start,
        day__lte=week_end
    ).values(
        'assignment', 'assignment__resource__name', 'assignment__position__name', 
        'assignment__position__project__code'
    ).annotate(hours=Sum('hours'))
    assignment_hours = [
        (
            assignment['assignment__position__project__code'],
            assignment['assignment__resource__name'],
            assignment['assignment__position__name'],
            assignment['hours']
        )
        for assignment in assignment_hours
    ]

    assignment_dates = Assignment.objects.filter(
        start__lte=week_start,
        end__gt=week_end
    ).order_by('end').values('position__project__code', 'position__name', 
    'resource__name', 'end')
    assignment_dates = [
        (
            assignment['position__project__code'],
            assignment['resource__name'],
            assignment['position__name'],
            assignment['end']
        )
        for assignment in assignment_dates
    ]

    project_revenues = Booking.objects.filter(
        day__lte=week_end,
        assignment__end__gt=week_end,
    ).values('assignment__position__project__code').annotate(
        sum=Coalesce(Sum(F('assignment__rate') * F('hours')), 0.0)
    )
    project_revenues = [
        (project_revenue['assignment__position__project__code'], project_revenue['sum'])
        for project_revenue in project_revenues
    ]

    project_costs = Booking.objects.filter(
        day__lte=week_end,
        assignment__end__gt=week_end,
    ).values('assignment__position__project__code').annotate(
        sum=Coalesce(Sum(F('assignment__resource__cone_rate') * F('hours')), 0.0)
    )
    project_costs = [
        (project_cost['assignment__position__project__code'], project_cost['sum'])
        for project_cost in project_costs
    ]

    open_risks = Risk.objects.filter(status='Open').count()

    context = {
        'assignment_hours': assignment_hours,
        'live_projects': live_projects,
        'assignment_dates': assignment_dates,
        'project_revenues': (
            [p[0] for p in project_revenues],
            [p[1] for p in project_revenues]
        ),
        'project_costs': (
            [p[0] for p in project_costs],
            [p[1] for p in project_costs]
        ),
        'open_risks': open_risks,
    }

    return render (request, 'ii_app/dashboard.html',context)

@login_required(login_url = 'sign_in')
def resources(request):
    query = request.GET.get("query")
    if query:
        resource = Resource.objects.filter(name__icontains = query) 
    else:
        resource = Resource.objects.all()
    context = {
        'resource':resource ,
    }

    return render (request, 'ii_app/resources.html', context)

@login_required(login_url = 'sign_in')
def resource_detail(request,name):
    
    assignments = Assignment.objects.filter(resource__name = name)

    context = {
        'assignments': assignments ,
    }

    return render (request, 'ii_app/resource_detail.html', context)

@login_required(login_url = 'sign_in')
def risk_form(request):
    form = RiskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('')

    return render (request, 'ii_app/risk_form.html', {'form':form})

@login_required(login_url = 'sign_in')
def update_risk_item(request,risk_id):
    item = Risk.objects.get(id=risk_id)
    form = RiskForm(request.POST or None,instance = item)

    if form.is_valid():
        form.save()
        return redirect(reverse('riskregister/'))

    return render (request, 'ii_app/risk_form.html', {'form':form, 'item':item})

@login_required(login_url = 'sign_in')
def delete_risk_item(request,risk_id):
    item = Risk.objects.get(id=risk_id)
  
    item.delete()

    return redirect(reverse('riskregister/'))

@login_required(login_url = 'sign_in')
def risk_register(request):

    query = request.GET.get('query') or ''

    risk_register = Risk.objects.filter
    (Q(owner__icontains = query) | Q(status__icontains = query))

    context = {
        'risk_register': risk_register,
    }
    return render (request, 'ii_app/risk_register.html', context)

@login_required(login_url = 'sign_in')
def margin(request):

    return render (request, 'ii_app/margin.html')

@login_required(login_url = 'sign_in')
def finances(request):

    query = request.GET.get('query') or ''
    
    projects = Project.objects.filter(title__icontains = query).order_by('code','title')
    
    context = {
        'projects': projects,
    }
    return render (request, 'ii_app/finances.html', context)
    
@login_required(login_url = 'sign_in')
def finance_detail (request, code):

    # project = Project.objects.get(code=code)
    project = get_object_or_404(Project, code = code)

    period_end = datetime.date.today().replace(day=1)
    period_start = (period_end - datetime.timedelta(days=1)).replace(day=1)

    total_bookings = Booking.objects.filter(
        assignment__position__project=project
    )
    period_bookings = total_bookings.filter(
        day__gte=period_start,
        day__lt=period_end
    )

    total_hours, period_hours = [
        bookings.aggregate(
            sum=Coalesce(Sum('hours'), 0.0)
        ).get('sum')
        for bookings in [total_bookings, period_bookings]
    ]
    
    total_revenue, period_revenue = [
        bookings.aggregate(
            sum=Coalesce(Sum(F('assignment__rate') * F('hours')), 0.0)
        ).get('sum')
        for bookings in [total_bookings, period_bookings]
    ]

    total_cost, period_cost = [
        bookings.aggregate(
            sum=Coalesce(Sum(F('assignment__resource__cone_rate') * F('hours')), 0.0)
        ).get('sum')
        for bookings in [total_bookings, period_bookings]
    ]

    if total_revenue:
        total_margin = round((total_revenue - total_cost) / total_revenue * 100, 2)
    else:
        total_margin = 0

    if period_revenue:
        period_margin = round((period_revenue - period_cost) / period_revenue * 100, 2)
    else:
        period_margin = 0 

    context = {
        'total_hours': total_hours,
        'period_hours': period_hours,
        'total_revenue': total_revenue,
        'period_revenue': period_revenue,
        'total_cost': total_cost,
        'period_cost': period_cost,
        'total_margin': total_margin,
        'period_margin': period_margin
    }

    return render (request, 'ii_app/finance_detail.html', context)

@login_required(login_url = 'sign_in')
def cv(request):
    resource = Resource.objects.all()

    context = {
        'resource': resource
    }

    return render (request, 'ii_app/cv.html', context)


@login_required(login_url = 'sign_in')
def search_bar (request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            resources = Resource.objects.filter(name__icontains = query)
            return render (request, 'ii_app/search_bar.html', {'resources': resources})

    else:
        print("your query did not return any results")
        return request (request, 'ii_app/search_bar.html', {})

@login_required(login_url = 'sign_in')
def bookings (request):

   query = request.GET.get('query') or ''
    
   resource_info = Assignment.objects.filter
   (Q(resource__name__icontains = query) |Q(position__project__code = query))
    
   context = {
        'resource_info': resource_info,
    }
   return render (request, 'ii_app/bookings.html', context)

@login_required(login_url = 'sign_in')
def booking_form(request,assignment_code):

    if request.GET.get('week'):
        return booking_week(request,assignment_code)
    
    # assignment = Assignment.objects.get(pk=assignment_code)
    assignment = get_object_or_404(Assignment, pk = assignment_code)
    week_start = date.today()
    week_start -= timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=4)
    day_dict = {
        'monday':week_start,
        'tuesday': week_start + timedelta(days = 1),
        'wednesday':  week_start + timedelta(days = 2),
        'thursday':  week_start + timedelta(days = 3),
        'friday':  week_start + timedelta(days = 4),
    }

    day_dict_2 = [value.strftime('%d-%m-%Y') for key,value in day_dict.items()]

    bookings = assignment.booking_set.filter(day__gte=week_start, day__lte=week_end)
    booking_dict = {booking.day.strftime('%A').lower():booking for booking in bookings}
   
    form = BookingForm(initial={key:value.hours for key,value in booking_dict.items()})
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            for key,value in form.cleaned_data.items():
                if key in booking_dict:
                    booking_dict[key].hours = value
                    booking_dict[key].save()
                else:
                    booking = assignment.booking_set.create(day = day_dict[key], hours = value)
            return redirect(f'/ii_app/bookings/{assignment_code}')
      
    context = {
        'form':form,
        'resource': assignment.resource.name,
        'week_end':week_end,
        'day_dict':day_dict_2,
        'zipped':zip(form,day_dict_2),
        'week':0,
        'project':assignment_code
    }

    return render (request, 'ii_app/booking_form.html', context)

@login_required(login_url = 'sign_in')
def booking_week(request,assignment_code):
    week = request.GET.get('week')
    try: 
        week = int(week)
        if week < 1: 
            raise ValueError
    except:
        week = 1
    assignment = Assignment.objects.get(pk=assignment_code)
    week_start = date.today()-timedelta(days = 7*week)
    week_start -= timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=4)
    day_dict = {
        'monday':week_start,
        'tuesday': week_start + timedelta(days = 1),
        'wednesday':  week_start + timedelta(days = 2),
        'thursday':  week_start + timedelta(days = 3),
        'friday':  week_start + timedelta(days = 4),
    }

    day_dict_2 = [value.strftime('%d-%m-%Y') for key,value in day_dict.items()]

    bookings = assignment.booking_set.filter(day__gte=week_start, day__lte=week_end)
    booking_dict = {booking.day.strftime('%A').lower():booking for booking in bookings}
   
    form = BookingForm(initial={key:value.hours for key,value in booking_dict.items()})

    context = {
        'form':form,
        'resource': assignment.resource.name,
        'week_end':week_end,
        'day_dict':day_dict_2,
        'zipped':zip(form,day_dict_2),
        'week': week,
        'project': assignment_code
    }

    return render (request, 'ii_app/booking_week.html', context)

@api_view(['GET','POST'])
def project_list_api (request):

    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many = True)
        return JsonResponse({'projects':serializer.data})
    
    if request.method == 'POST':
        serializer = ProjectSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET','PUT', 'DELETE'])
def project_list_api_detail (request,id):

    try: 
        project = Project.objects.get(pk = id)
    except Project.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

# get all the projects 
# serialize them 
# return json

# from django.forms import modelformset_factory 
# from .models import Position, Contract, Booking, Invoice
# from .forms import FileUploadForm
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.shortcuts import HttpResponse
# from django.template import loader
# from multiprocessing.sharedctypes import Value
# import requests

# @login_required(login_url = 'sign_in')
# def api(request):
   
#     api = requests.get('https://api.covid19api.com/countries').json()
#     context = {
#         'api':api
#     }
#     return render (request, 'ii_app/api.html', context)

