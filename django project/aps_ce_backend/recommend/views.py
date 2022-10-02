from operator import index
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Student
from .serializers import StudentSerializer
# Create your views here.

import re
import requests
from pandasql import sqldf

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


def dropUnUseRecc(df):
    q_for_Computer_ContrainSub = "SELECT * FROM (SELECT * FROM df WHERE curriculum = 'วิศวกรรมคอมพิวเตอร์' OR curriculum = 'วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)') WHERE subject_id NOT LIKE '90%'"
    df = sqldf(q_for_Computer_ContrainSub)
    return df

@csrf_exempt
def addStudent(df):
    df = dropUnUseRecc(df)
    df['grade'] = df['grade'].fillna('Zero')
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
            print(f'save {student_serializer.data}')
        else:
            res = "Failed to add"
            print(res)
            return res
    res = 'Complete add' 
    return res

def generateModel(request):
    return JsonResponse('HI', safe=False)

        

