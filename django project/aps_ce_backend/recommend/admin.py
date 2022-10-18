from django.contrib import admin
from .models import Student,Subject_Data,SurpriseModel
# Register your models here.

admin.site.register(Student)
admin.site.register(Subject_Data)
admin.site.register(SurpriseModel)