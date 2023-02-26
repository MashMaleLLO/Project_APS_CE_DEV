from email.policy import default
from statistics import mode
from django.db import models
from picklefield.fields import PickledObjectField
from pytz import timezone
import pytz
from datetime import datetime
import bcrypt
# Create your models here.
class Student_Grade(models.Model):
      student_id = models.CharField(max_length=300)
      subject_id = models.CharField(max_length=20)
      grade = models.CharField(max_length=10, default='Zero')
      semester = models.CharField(max_length=5)
      year = models.CharField(max_length=10)

class Student_Data(models.Model):
      student_id = models.CharField(max_length=300)
      curriculum = models.CharField(max_length=100)
      status = models.CharField(max_length=100, default='ungraduate')
      career = models.CharField(max_length=100, default='Zero')
      start_year = models.CharField(max_length=100, default='Zero')
      curriculum_year = models.CharField(max_length=100, default='Zero')


class Subject_Data(models.Model):
      subject_id = models.CharField(max_length=300)
      subject_name_thai = models.CharField(max_length=600)
      subject_name_eng = models.CharField(max_length=500)
      abstract = models.CharField(max_length=3000)
      subject_key = models.CharField(max_length=200)
      year = models.CharField(max_length=4)
      subject_class = models.CharField(max_length=10, default='อื่นๆ')

class SurpriseModel(models.Model):
      name = models.CharField(max_length=300, default='rec_model')
      curriculum = models.CharField(max_length=100, default='Zero')
      rmse = models.CharField(max_length=100, default='Zero')
      create_date = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Bangkok')))
      update_date = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Bangkok')))
      del_flag = models.CharField(max_length=10, default=0)
      type_pred = models.CharField(max_length=100, default='Zero')
      rec_model = PickledObjectField(default='Zero')

      def save(self, *args, **kwargs):
            self.update_date = datetime.now(pytz.timezone('Asia/Bangkok'))
            return super().save(*args, **kwargs)
      
class CareerModel(models.Model):
      name = models.CharField(max_length=300, default='rec_model')
      curriculum = models.CharField(max_length=100, default='Zero')
      accuracy = models.CharField(max_length=100, default='Zero')
      create_date = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Bangkok')))
      update_date = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Bangkok')))
      del_flag = models.CharField(max_length=10, default=0)
      career_model = PickledObjectField(default='Zero')

      def save(self, *args, **kwargs):
            self.update_date = datetime.now(pytz.timezone('Asia/Bangkok'))
            return super().save(*args, **kwargs)

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

class Rec_User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        hashpw = bcrypt.hashpw(password.encode('utf-8'), salt=self.salt)
        self.password = hashpw.decode('utf-8')
        
        
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))