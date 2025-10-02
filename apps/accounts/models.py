from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin","Admin"
        TEACHER = "teacher","Teacher"
        STUDENT = "student","Student"

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.STUDENT)

    phone = models.CharField(max_length=15,unique=True, blank=True, null=True)


    def __str__(self):
        return self.username