from django.contrib import admin
from .models import Student_Data, Student_Grade, Rec_User, CSV_File,Subject_Data,SurpriseModel
# Register your models here.

admin.site.register(Student_Data)
admin.site.register(Student_Grade)
admin.site.register(Rec_User)
admin.site.register(CSV_File)
admin.site.register(Subject_Data)
admin.site.register(SurpriseModel)