import os

from django.db import models
from django.contrib.auth import get_user_model

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

