from django.db import models

# Create your models here.
class Student(models.Model):
      student_id = models.CharField(max_length=300)
      subject_id = models.CharField(max_length=20)
      grade = models.CharField(max_length=10, default='Zero')
      semester = models.CharField(max_length=5)
      year = models.CharField(max_length=10)
      curriculum = models.CharField(max_length=100)

