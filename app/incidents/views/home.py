import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
#from todo.forms import SearchForm
from todo.models import Task, TaskList
from todo.utils import staff_check
#from django.views.generic import TemplateView


@login_required
@user_passes_test(staff_check)
def dashboard_functions(request) -> HttpResponse:
        
        if request.user.is_superuser:
                task_count = Task.objects.filter(completed=0).count()
        else:
                task_count = (Task.objects.filter(completed=0)
                                .filter(task_list__group__in=request.user.groups.all()).count())
                
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
        "daily_calls": daily_calls,
        "task_unassigned": task_unassigned,
        "task_count": task_count,
        }
        return render(request, "home.html", context)