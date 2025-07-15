from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.CharField(max_length=100)

class Teacher(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # (Optional: Use hashed password in real apps)
