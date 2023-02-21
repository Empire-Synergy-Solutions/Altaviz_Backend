import datetime

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
#from todo.forms import SearchForm
from incidents.models import Task, TaskList
from incidents.utils import staff_check
from django.views.generic import TemplateView, ListView


@login_required
@user_passes_test(staff_check)
def dashboard_functions(request) -> HttpResponse:
        
        if request.user.is_superuser:
                task_count = Task.objects.filter(completed=0).count()
                #latest_fault_list = Task.objects.order_by('-created_date')[:5]
        else:
                task_count = (Task.objects.filter(completed=0)
                                .filter(task_list__group__in=request.user.groups.all()).count())
                #latest_fault_list = (Task.objects.order_by('-created_date')[:5]
                                     #.filter(task_list__group__in=request.user.groups.all()))
        if request.user.is_superuser:
                task_unassigned = Task.objects.filter(assigned_to=None).count()
        else:
                task_unassigned = (Task.objects.filter(assigned_to=None)
                                .filter(task_list__group__in=request.user.groups.all()).count())
                
        if request.user.is_superuser:
                daily_calls = Task.objects.filter(created_date=timezone.now()).count()
        else:
                daily_calls = (Task.objects.filter(created_date=timezone.now)
                                .filter(task_list__group__in=request.user.groups.all()).count())
         
        context = {
        #"lists": lists,
        #"thedate": thedate,
        #"latest_fault_list":latest_fault_list,
        "daily_calls": daily_calls,
        "task_unassigned": task_unassigned,
        "task_count": task_count,
        }
        return render(request, "home.html", context)

#class NotificationListView(ListView):
    #model = Task
    #template_name = "navigation.html"
    #queryset = Task.objects.order_by('-created_date')
    
    #def get_queryset(self, *args, **kwargs):
        #qs = super(NotificationListView, self).get_queryset(*args, **kwargs)
        #qs = qs.order_by("-created_date")
        #return qs