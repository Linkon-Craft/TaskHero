from django.urls import path

from . import views

app_name="task"

urlpatterns={
    path('', views.home, name='home'),
    path('all/task/', views.all_task, name='all_task'),
    path('tasks/<int:task_id>/', views.task_details, name='task_details'),
    path('add/task/', views.add_task, name='add_task'),
    path('update/task/<int:task_id>/', views.update_task, name='update_task'),
    path('confirm/delete/<int:task_id>/', views.confirm_delete, name='confirm_delete'),
    path('delete/task/<int:task_id>/', views.delete_task, name='delete_task')
}