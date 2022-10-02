from operator import index
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Student
from .serializers import StudentSerializer
# Create your views here.

import re
import requests
import pandas as pd
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
            return JsonResponse(students_serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})
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

def queryBycurriculum(df):
  curriculums = list(df["curriculum"].unique())
  dfs = {}
  for i in curriculums:
    q = "SELECT * FROM df WHERE curriculum = '{0}'".format(i)
    temp = sqldf(q)
    dic = {i:[]}
    dic[i].append(temp)
    dfs.update(dic)
  return dfs


def transfromGrade(df):
  df.loc[df["grade"] == "A", "grade"] = 4
  df.loc[df["grade"] == "S", "grade"] = 4
  df.loc[df["grade"] == "T(A)", "grade"] = 4

  df.loc[df["grade"] == "B+", "grade"] = 3.5
  df.loc[df["grade"] == "T(B+)", "grade"] = 3.5

  df.loc[df["grade"] == "B+", "grade"] = 3.5
  df.loc[df["grade"] == "T(B+)", "grade"] = 3.5

  df.loc[df["grade"] == "B", "grade"] = 3
  df.loc[df["grade"] == "T(B)", "grade"] = 3

  df.loc[df["grade"] == "C+", "grade"] = 2.5
  df.loc[df["grade"] == "T(C+)", "grade"] = 2.5

  df.loc[df["grade"] == "C", "grade"] = 2
  df.loc[df["grade"] == "T(C)", "grade"] = 2

  df.loc[df["grade"] == "D+", "grade"] = 1.5
  df.loc[df["grade"] == "T(D+)", "grade"] = 1.5

  df.loc[df["grade"] == "D", "grade"] = 1
  df.loc[df["grade"] == "T(D)", "grade"] = 1

  df.loc[df["grade"] == "F", "grade"] = 0
  df.loc[df["grade"] == "T(F)", "grade"] = 0
  df.loc[df["grade"] == "U", "grade"] = 0

  return df


def transfromAlldfs(dfs):
  for i in dfs:
    dfs[i][0] = transfromGrade(dfs[i][0])
  return dfs


@csrf_exempt
def generateModel(request):
    qdata = list(Student.objects.all().values())
    df = pd.DataFrame(qdata)
    dfs = queryBycurriculum(df)
    dfs = transfromAlldfs(dfs)
    
    # Check Function QueryByCurriculum------------------
    # temp = {}
    # for i in dfs:
    #     a = dfs[i][0]
    #     # a = a.head()
    #     print(a['grade'])
    #     a = a.values.tolist()
    #     di = {i:a}
    #     temp.update(di)

    return JsonResponse(temp , safe=False, json_dumps_params={'ensure_ascii': False})

        
