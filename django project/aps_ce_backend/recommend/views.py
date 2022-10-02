from operator import index
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Student
from .serializers import StudentSerializer
# Create your views here.

import re
import requests

def catch():
    lis = ['a','b','c']
    return lis

@csrf_exempt
def studentApi(request,id=0):
    if request.method=='GET':
        print(id)
        if id == 0:
            students = Student.objects.all()
            students_serializer = StudentSerializer(students,many=True)
            return JsonResponse(students_serializer.data, safe=False)
        else:
            student = Student.objects.get(student_id=id)
            student_serializer = StudentSerializer(student)
            return JsonResponse(student_serializer.data, safe=False)

@csrf_exempt
def addStudent(df):
    for index,student in df.iterrows():
        dic = {
            "student_id":student['student_id'],
            "subject_id":student['subject_id'],
            "grade":student['grade'],
            "semester":student['semester'],
            "year":student['year'],
            "curriculum":student['curriculum']
        }
        student_serializer = StudentSerializer(data=dic)
        if student_serializer.is_valid():
            student_serializer.save()
        else:
            res = "Failed to add"
            return res
    res = 'Complete add' 
    return res
        

