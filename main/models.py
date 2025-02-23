from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=(("to do", "to do"),("in progress","in progress"),("done","done")), default="to do")
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True,null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title