from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['completed', '-updated']

    def get_absolute_url(self):
        return reverse('complete_task', kwargs={"pk": self.id})
