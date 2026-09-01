import os

from django.db import models
from django.contrib.auth import get_user_model
from datetime import date, datetime, timedelta
from django.utils import timezone


User = get_user_model()

class Status(models.TextChoices):
    TO_DO = "TD", "To_Do"
    IN_PROGRESS = "IN_PRGRS", "In_Progress"
    COMPLETED = "COMPTD", "Completed"

class Priority(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MDIUM", "Medium"
    HIGH = "HIGH", "High"



class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date =  models.DateTimeField()
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.TO_DO)
    priority = models.CharField(max_length=50, choices=Priority.choices, default=Priority.MEDIUM)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "task")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
    
    @property
    def is_overdue(self):
        return (
            self.status != Status.COMPLETED
            and timezone.now() > self.due_date
        )


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        DUE_SOON = "DUE_SOON", "Due Soon"
        DUE_TODAY = "DUE_TODAY", "Due Today"
        OVERDUE = "OVERDUE", "Overdue"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)

    message = models.CharField(max_length=255)

    notification_type = models.CharField(max_length=20,choices=NotificationType.choices)

    created_at = models.DateTimeField(auto_now_add=True)

    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.message}"