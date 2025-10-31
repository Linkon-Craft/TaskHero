from functools import wraps

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Task
from .forms import TaskForm

def user_is_task_author(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        task = get_object_or_404(Task, pk=task_id)

        if task.added_by != request.user:
            messages.error(request, "You need to be logged in to perform that action.")
            return redirect("account:login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def home(request):
    return render(request, "taskhero/home.html")


def all_task(request):
    task = Task.objects.all()
    return render(request, "taskhero/all_task.html", context=task)

@login_required
def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "taskhero/task_details.html", context=task)

@login_required
def add_task(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST, request.Files)
        if form.is_valid:
            task = form.save(commit=False)
            task.added_by = request.User
            task.save()
            return redirect('task:all_task')
    return render(request, "taskhero/add_task.html", {"form":form})

@login_required
@user_is_task_author
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task:task_details')
    
    context = {
        'form':form,
        'task':task
    }
    return render(request, "taskhero/update_task.html", context)


@login_required
@user_is_task_author
def confirm_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "taskhero/comfirm-delete.html", {'task': task})


@login_required
@user_is_task_author
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.delete()
    return redirect('task:all_task')