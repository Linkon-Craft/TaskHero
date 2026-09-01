from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            },
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=[
            "%Y-%m-%dT%H:%M",
        ],
    )

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "status", "priority"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder":"Enter your task title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder":"Describe your task..."
                }
            ),

            "status": forms.Select(
                attrs={
                    "class":"form-select"
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class":"forms-select"
                }
            )
        
        }