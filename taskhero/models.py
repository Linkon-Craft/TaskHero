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
    due_date = models.DateField()
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.TO_DO)
    priority = models.CharField(max_length=50, choices=Priority.choices, default=Priority.MEDIUM)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "task")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}, {self.description}"
    
    # @property
    # def can_still_be_edited(self):
    #     now = timezone.now()
    #     return now - self.created_at <= timedelta(minutes=5)
    
    def check_and_update_status(self):
        if self.status != Status.COMPLETED and date.today() >= self.due_date:
            self.status = Status.COMPLETED
            self.save(update_fields=["status"])
    