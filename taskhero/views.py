from django.db.models import Q

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


from .models import Task, Notification
from .forms import TaskForm



def home(request):
    return render(request, "taskhero/home.html")

@login_required
def all_task(request):
    query = request.GET.get('q', '')
    tasks = Task.objects.filter(added_by=request.user)
    
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(status__icontains=query) |
            Q(priority__icontains=query)
        )
    
    context = {
        'query': query,
        'all_task': tasks
    }

    
    return render(request, "taskhero/all_task.html", context)

@login_required
def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id, added_by=request.user)
    return render(request, "taskhero/task_details.html", {'task':task})

@login_required
def add_task(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.added_by = request.user
            task.save()
            return redirect('taskhero:all_task')
    return render(request, "taskhero/add_task.html", {"form":form})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, added_by=request.user)
    form = TaskForm(instance=task)
    # if not task.can_still_be_edited:
    #     messages.error(request, "You can no longer edit this task")
    #     return redirect('taskhero:all_task')
    
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)

        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('taskhero:all_task')
    
    context = {
        'form':form,
        'task':task
    }
    return render(request, "taskhero/update_task.html", context)


@login_required
def confirm_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, added_by=request.user)
    return render(request, "taskhero/comfirm-delete.html", {'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, added_by=request.user)
    if request.method == "POST":
        task.delete()
    return redirect('taskhero:all_task')


@login_required
def get_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user,
        read=False
    )

    data = [
        {
            "id": n.id,
            "message": n.message,
            "type": n.notification_type,
            "task_id": n.task_id,
            "created_at": n.created_at.isoformat(),
        }
        for n in notifications
    ]

    return JsonResponse(data, safe=False)