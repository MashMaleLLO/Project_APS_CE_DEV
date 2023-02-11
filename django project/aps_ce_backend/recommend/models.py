from email.policy import default
from statistics import mode
from django.db import models
from picklefield.fields import PickledObjectField
from pytz import timezone
import pytz
from datetime import datetime
# Create your models here.
class Student(models.Model):
      student_id = models.CharField(max_length=300)
      subject_id = models.CharField(max_length=20)
      grade = models.CharField(max_length=10, default='Zero')
      semester = models.CharField(max_length=5)
      year = models.CharField(max_length=10)
      curriculum = models.CharField(max_length=100)
      status = models.CharField(max_length=100, default='ungraduate')
      career = models.CharField(max_length=100, default='Zero')
      start_year = models.CharField(max_length=100, default='Zero')

class Subject_Data(models.Model):
      subject_id = models.CharField(max_length=300)
      subject_name_thai = models.CharField(max_length=600)
      subject_name_eng = models.CharField(max_length=500)
      abstract = models.CharField(max_length=3000)
      subject_key = models.CharField(max_length=200)
      year = models.CharField(max_length=4)
      subject_class = models.CharField(max_length=10, default='อื่นๆ')

class SurpriseModel(models.Model):
      args = PickledObjectField()

class CSV_File(models.Model):
      name = models.CharField(max_length=300)
      upload_date = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Bangkok')))
      update_date = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Bangkok')))
      del_flag = models.CharField(max_length=10)
      type_data = models.CharField(max_length=100)
      file = PickledObjectField()

      def save(self, *args, **kwargs):
            self.update_date = datetime.now(pytz.timezone('Asia/Bangkok'))
            return super().save(*args, **kwargs)

