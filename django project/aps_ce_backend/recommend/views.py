from asyncio import constants
from cgi import test
from pyexpat import model
from unittest.util import safe_repr
from urllib import response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Student_Data, Student_Grade,Subject_Data, SurpriseModel, CSV_File, CareerModel
from .serializers import StudentGradeSerializer, StudentSerializer, SubjectSerializer
from rest_framework.parsers import JSONParser
from django.db.models import Q
from datetime import date
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
# Create your views here.



import re
import requests
import pandas as pd
from pandasql import sqldf
import pickle as cPickle
import json
import joblib

from surprise import Dataset
from surprise import Reader
from surprise import SVD, accuracy
from surprise.model_selection import cross_validate
from sklearn.model_selection import train_test_split as tt_split
from surprise.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV as gd_career
from sklearn.model_selection import KFold
from surprise.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics  import f1_score,accuracy_score
from sklearn import preprocessing
import numpy as np

from rest_framework import generics, status, authentication, permissions
import jwt

from backend import view as backend

def catch():
    lis = ['a','b','c']
    return lis

@csrf_exempt
def surpriseModel(request,id=0):
    if request.method=='GET':
        print(id)
        if id == 0:
            res = []
            model = list(SurpriseModel.objects.all().values())
            for i in model:
              dic = {
                "id": i['id'],
                "name" : i['args']['name'],
                "rmse" : i['args']['rmse'],
                "curriculum": i['args']['curriculum'],
                "type":i['args']['type']
              }
              res.append(dic)
            return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
    return JsonResponse("BAD REQUEST", safe=False)

@csrf_exempt
def file_api(request, id=0):
  if request.method=='GET':
    if id == 0:
      res = pd.DataFrame(list(CSV_File.objects.filter(del_flag= '0').values()))
      res = res[['id','name', 'upload_date', 'update_date', 'del_flag', 'type_data']].to_dict('records')
      res = { "message" : res, "status": status.HTTP_200_OK }
    else:
      this_file = list(CSV_File.objects.filter(id = id).values())
      if this_file == []:
        res = {"message" : f'cant find the file with id {id}', "status" : status.HTTP_400_BAD_REQUEST}
      else:
        content = this_file[0]['file']
        this_file = pd.DataFrame(this_file)
        content = cPickle.loads(content)
        content = content.to_dict('records')
        print(len(content))
        res = this_file[['id','name', 'upload_date', 'update_date', 'del_flag', 'type_data']].to_dict('records')[0]
        res = { "message" : {"file_information" : res, "file_content" : content}, "status": status.HTTP_200_OK }
        print(res)
  elif request.method=='DELETE':
    if id == 0:
      res = {"message" : "Pls enter file id" , "status" : status.HTTP_400_BAD_REQUEST}
    else:
      this_file = list(CSV_File.objects.filter(id = id).values())
      if this_file == []:
        res = {"message" : f'Can not find file with id {id}' , "status" : status.HTTP_400_BAD_REQUEST}
      else:
        this_file = CSV_File.objects.get(id = id)
        this_file.del_flag = '1'
        this_file.save()
        res = {"message" : f'Delete file id {this_file.name} Complete', "status" : status.HTTP_200_OK}
  else:
    res = {"message":"Request method not match", "status": status.HTTP_400_BAD_REQUEST}
  return JsonResponse(res, safe=False)

@csrf_exempt
def file_content_edit(request, id = 0, index="Default"):
  if request.method == 'PUT':
    try:
      inform = json.loads(request.body)
      action = inform["action"]
      index = inform["index"]
      file_content = inform['content']
    except:
      res = {"meassage" : "Can not find any index pls resummit again", "status" : status.HTTP_400_BAD_REQUEST}
      return JsonResponse(res, safe=False)
    if index == "Default" or id == 0: 
      res = {"meassage" : "Can not find any index pls resummit again", "status" : status.HTTP_400_BAD_REQUEST}
    else:
      this_file = list(CSV_File.objects.filter(id = id).values())
      if this_file == []:
        res = {"message" : f'Can not find any file with id = {id}', "status" : status.HTTP_400_BAD_REQUEST}
      else:
        original_file = CSV_File.objects.get(id = id)
        this_file = this_file[0]['file']
        this_file = cPickle.loads(this_file)
        content = pd.DataFrame(this_file)
        if action == "Add":
          new_content = pd.DataFrame([file_content])
          try:
            content = pd.concat([content, new_content], ignore_index=True)
          except:
            res = {"message" : "Error in process append content", "status" : status.HTTP_400_BAD_REQUEST}
            return JsonResponse(res, safe=False)
        elif action == "Edit":
          new_content = pd.DataFrame([file_content])
          try:
            content.iloc[index] = new_content
          except:
            res = {"message" : "Error in process edit content", "status" : status.HTTP_400_BAD_REQUEST}
            return JsonResponse(res, safe=False)
        elif action == "Delete":
          try:
            content = content.drop(index=index)
            content = content.reset_index(drop=True)
          except:
            res = {"message" : "Error in process delete content", "status" : status.HTTP_400_BAD_REQUEST}
            return JsonResponse(res, safe=False)
        original_file.file = cPickle.dumps(content)
        original_file.save()
        res = {"message" : f'Complete {action}', "status" : status.HTTP_200_OK}
  else:
    res = {"message":"Request method not match", "status": status.HTTP_400_BAD_REQUEST}
  return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def student_data_api(request, id='all', curri='Default'):
  if request.method == 'GET':
    if request.body:
      body = json.loads(request.body)
      curri = body['curriculum']
    if id == 'all':
      if curri == 'All':
        student = Student_Data.objects.all()
        student_serializer = StudentSerializer(student, many=True)
        res = {"message":student_serializer.data, "status": status.HTTP_200_OK}
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
      elif curri == 'Default':
        student = Student_Data.objects.filter(curriculum__in = ['วิศวกรรมคอมพิวเตอร์', 'วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)'])
        student_serializer = StudentSerializer(student, many=True)
        res = {"message":student_serializer.data, "status": status.HTTP_200_OK}
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
      else:
        student = Student_Data.objects.filter(curriculum = curri)
        student_serializer = StudentSerializer(student, many=True)
        res = {"message":student_serializer.data, "status": status.HTTP_200_OK}
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
      student = list(Student_Data.objects.filter(student_id = id).values())
      if student == []:
        res = {"message":f'cant not find student id {id}', "status": status.HTTP_404_NOT_FOUND}
        return JsonResponse(res, safe=False)
      else:
        student = student[0]['id']
        student = Student_Data.objects.get(id=student)
        student_serializer = StudentSerializer(student)
        res = {"message":student_serializer.data, "status": status.HTTP_200_OK}
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
  elif request.method == 'PUT':
    if id == 0:
      res = {"message":"pls enter student id to update", "status": status.HTTP_400_BAD_REQUEST}
      return JsonResponse(res, safe=False)
    else:
      student = list(Student_Data.objects.filter(student_id = id).values())
      if student == []:
        res = {"message":f'cant not find student id {id}', "status": status.HTTP_404_NOT_FOUND}
        return JsonResponse(res, safe=False)
      else:
        student = student[0]['id']
        student = Student_Data.objects.get(id = student)
        student_data=JSONParser().parse(request)
        student_serializer = StudentSerializer(student, data=student_data)
        if student_serializer.is_valid():
          student_serializer.save()
          res = {"message": f'Update {student_serializer.data}', "status": status.HTTP_200_OK}
          return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
          res = {"message": f'Serailizer failed at {student_serializer.data}', "status": status.HTTP_400_BAD_REQUEST}
          return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
  elif request.method == 'DELETE':
    if id == 0:
      res = {"message":"pls enter student id to update", "status": status.HTTP_400_BAD_REQUEST}
      return JsonResponse(res, safe=False)
    else:
      student = list(Student_Data.objects.filter(student_id = id).values())
      if student == []:
        res = {"message":f'cant not find student id {id}', "status": status.HTTP_404_NOT_FOUND}
        return JsonResponse(res, safe=False)
      else:
          student = student[0]['id']
          student = Student_Data.objects.get(id = student)
          student_serializer = StudentSerializer(student)
          student.delete()
          res = {"message": f'Delete {student_serializer.data}', "status": status.HTTP_200_OK}
          return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
  return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def student_grade_api(request, st_id='all', su_id='all'):
  if request.method == 'GET':
    if st_id == 'all':
      student_data = pd.DataFrame(list(Student_Data.objects.all().values()))
      student_grade = pd.DataFrame(list(Student_Grade.objects.all().values()))
      result = pd.merge(student_grade, student_data, how='left', on='student_id')
      result = result[['student_id', 'subject_id', 'grade', 'semester', 'year', 'curriculum']]
      data_list = result.to_dict('records')
      res = {"message":data_list, "status": status.HTTP_200_OK}
      return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
      if su_id == 'all':
        student_data = pd.DataFrame(list(Student_Data.objects.all().values()))
        student_grade = pd.DataFrame(list(Student_Grade.objects.filter(student_id = st_id).values()))
        result = pd.merge(student_grade, student_data, how='left', on='student_id')
        result = result[['student_id', 'subject_id', 'grade', 'semester', 'year', 'curriculum']]
        data_list = result.to_dict('records')
        res = {"message":data_list, "status": status.HTTP_200_OK}
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
      else:
        student = list(Student_Grade.objects.filter(student_id = st_id, subject_id = su_id).values())
        if student == []:
          res = {"message":f'cant not find student id {st_id} with sub id {su_id}', "status": status.HTTP_404_NOT_FOUND}
          return JsonResponse(res, safe=False)
        else:
          student_data = pd.DataFrame(list(Student_Data.objects.all().values()))
          student_grade = pd.DataFrame(list(Student_Grade.objects.filter(student_id = st_id, subject_id = su_id).values()))
          result = pd.merge(student_grade, student_data, how='left', on='student_id')
          result = result[['student_id', 'subject_id', 'grade', 'semester', 'year', 'curriculum']]
          data_list = result.to_dict('records')
          res = {"message":data_list, "status": status.HTTP_200_OK}
          return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
  elif request.method == 'PUT':
    if st_id == 0:
      res = {"message":"pls enter student id to update", "status": status.HTTP_400_BAD_REQUEST}
      return JsonResponse(res, safe=False)
    else:
      if su_id == 0:
        res = {"message":"pls enter sudject id to update", "status": status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)
      else:
        student_data=JSONParser().parse(request)
        student = list(Student_Grade.objects.filter(student_id = st_id, subject_id = su_id).values())
        if student == []:
          res = {"message":f'cant not find student id {st_id} with sub id {su_id}', "status": status.HTTP_404_NOT_FOUND}
          return JsonResponse(res, safe=False)
        else:
          student = student[0]['id']
          student = Student_Grade.objects.get(id=student)
          student_serializer = StudentGradeSerializer(student, data=student_data)
          if student_serializer.is_valid():
            student_serializer.save()
            res = {"message": f'Update {student_serializer.data}', "status": status.HTTP_200_OK}
            return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
          else:
            res = {"message": f'Serailizer failed at {student_serializer.data}', "status": status.HTTP_400_BAD_REQUEST}
            return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
  elif request.method == 'DELETE':
    if st_id == 0:
      res = {"message":"pls enter student id to delete", "status": status.HTTP_400_BAD_REQUEST}
      return JsonResponse(res, safe=False)
    else:
      if su_id == 0:
        res = {"message":"pls enter sudject id to delete", "status": status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)
      else:
        student = list(Student_Grade.objects.filter(student_id = st_id, subject_id = su_id).values())
        if student == []:
          res = {"message":f'cant not find student id {st_id} with sub id {su_id}', "status": status.HTTP_404_NOT_FOUND}
          return JsonResponse(res, safe=False)
        else:
          student = student[0]['id']
          student = Student_Grade.objects.get(id=student)
          student_serializer = StudentGradeSerializer(student)
          student.delete()
          res = {"message": f'Delete {student_serializer.data}', "status": status.HTTP_200_OK}
          return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})


def career_update(df):
  student = Student_Data.objects.all()
  student = list(student.values())
  df_student_data = pd.DataFrame(student)
  career_df = df
  join_q = "select df_student_data.student_id, df_student_data.curriculum, df_student_data.status, career_df.job as career, start_year, curriculum_year from df_student_data left join career_df on df_student_data.student_id = career_df.student_id"
  final_df = sqldf(join_q)
  for index,student in final_df.iterrows():
    if student['career'] is None:
      dic = {
        "student_id":student['student_id'],
        "curriculum":student['curriculum'],
        "status":student['status'],
        "career":"Zero",
        "start_year":student['start_year'],
        "curriculum_year": student['curriculum_year']
      }
    else:
      dic = {
        "student_id":student['student_id'],
        "curriculum":student['curriculum'],
        "status":student['status'],
        "career":student['career'],
        "start_year":student['start_year'],
        "curriculum_year": student['curriculum_year']
      }
    this_student = list(Student_Data.objects.filter(student_id = dic['student_id']).values())
    if this_student == []:
      student_data_serializer = StudentSerializer(data=dic)
      if student_data_serializer.is_valid():
          student_data_serializer.save()
          print(f'save {student_data_serializer.data}')
      else:
          res = False
          return res
    else:
      s_id = this_student[0]['id']
      this_student = Student_Data.objects.get(id=s_id)
      student_data_serializer = StudentSerializer(this_student, data=dic)
      if student_data_serializer.is_valid():
        student_data_serializer.save()
        print(f'update {student_data_serializer.data}')
      else:
        res = False
        print("Update failed",res,student_data_serializer)
        return res
  res = True
  return res




@csrf_exempt
def getStudentWithJob(request):
  student = list(Student_Data.objects.filter(~Q(career='Zero')).values())
  if student == []:
    res = {"message": "There is nothing to return", "status": status.HTTP_400_BAD_REQUEST}
    return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
  else:
    df = pd.DataFrame(student)
    q = "SELECT student_id, career from df"
    df = sqldf(q)
    student = df.values.tolist()
    res = {"message": student, "status": status.HTTP_200_OK}
  return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def subjectApi(request,id=0):
  if request.method == 'GET':
    print(id)
    if id == 0:
      subjects = Subject_Data.objects.all()
      subjects_serializer = SubjectSerializer(subjects, many=True)
      res = {"message": subject_serializer.data, "status": status.HTTP_200_OK}
      return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
      subject = Subject_Data.objects.get(subject_id = id)
      subject_serializer = SubjectSerializer(subject)
      res = {"message": subject_serializer.data, "status": status.HTTP_200_OK}
      return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
  elif request.method == 'POST':
    subject_data=JSONParser().parse(request)
    subject_serializer=SubjectSerializer(data=subject_data)
    if subject_serializer.is_valid():
      subject_serializer.save()
      res = {"message": f'save {subject_serializer.data} success pls manualy update subject groups.', "status": status.HTTP_200_OK}
    else:
      res = {"message": subject_serializer.errors, "status": status.HTTP_400_BAD_REQUEST}
    return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
  elif request.method == 'PUT':
    if id == 0:
      res = {"message": "pls fill in subject id", "status": status.HTTP_400_BAD_REQUEST}
    else:
      this_subject = list(Subject_Data.objects.filter(subject_id = id).values())
      if this_subject == []:
        res = {"message": f'can\'t find subject with id : {id}', "status": status.HTTP_400_BAD_REQUEST}
      else:
        subject_data=JSONParser().parse(request)
        subject_serializer = SubjectSerializer(this_subject, data = subject_data)
        if subject_serializer.is_valid():
          subject_serializer.save()
          res = {"message":"complete update subject info pls manualy update subject groups.", "status": status.HTTP_200_OK}
        else:
          res = {"message": subject_serializer.errors, "status": status.HTTP_400_BAD_REQUEST}
    return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
    


@csrf_exempt
def addStudent_grade(df):
    # df = dropUnUseRecc(df)
    df['grade'] = df['grade'].fillna('Zero')
    for index,student in df.iterrows():
        strt = '0'
        subId = student['subject_id']
        if len(subId) < 8:
          strt += student['subject_id']
          subId = strt
        dic = {
            "student_id":student['student_id'],
            "subject_id":subId,
            "grade":student['grade'],
            "semester":student['semester'],
            "year":student['year']
        }
        this_student = Student_Grade.objects.filter(student_id = dic['student_id'])
        this_student_n_sub = Student_Grade.objects.filter(student_id = dic['student_id'], subject_id = dic['subject_id'])
        if not this_student or not this_student_n_sub:
          student_grade_serializer = StudentGradeSerializer(data=dic)
          if student_grade_serializer.is_valid():
              student_grade_serializer.save()
              print(f'save {student_grade_serializer.data}')
          else:
              res = False
              print(res)
              return res
        else:
          s_id = list(this_student_n_sub.values())[0]['id']
          student_grade_serializer = StudentGradeSerializer(Student_Grade.objects.get(id=s_id), data = dic)
          if student_grade_serializer.is_valid():
            student_grade_serializer.save()
            print(f'update {student_grade_serializer.data}')
          else:
            res = False
            print("Update failed",res)
            return res
    res = True 
    return res

def addStudent_data(df):
  todays_date = date.today()
  base_year = todays_date.year + 543 - 4
  base_year = "'" + str(base_year) + "'"
  df = df
  q = f'select student_id, curriculum, case when min(year) < {base_year} then \'graduate\' else \'ungraduate\' end as status,min(year) as start_year from df group by student_id'
  df1 = sqldf(q)
  for index,student in df1.iterrows():
    dic = {
      "student_id":student['student_id'],
      "curriculum":student['curriculum'],
      "status":student['status'],
      "career":"Zero",
      "start_year":student['start_year'],
      "curriculum_year":'Zero'
    }
    this_student = Student_Data.objects.filter(student_id = dic['student_id'])
    start_year = int(student['start_year'])
    while start_year % 4 != 0:
      start_year = start_year - 1
    curri_year = start_year
    dic['curriculum_year'] = str(curri_year)
    if not this_student:
      student_serializer = StudentSerializer(data=dic)
      if student_serializer.is_valid():
        student_serializer.save()
        print(f'save {student_serializer.data}')
      else:
        res = False
        print(f'cant save {student_serializer.data}')
        return res
    else:
      s_id = list(this_student.values())[0]['id']
      student_serializer = StudentSerializer(Student_Data.objects.get(id = s_id), data = dic)
      if student_serializer.is_valid():
        student_serializer.save()
        print(f'update {student_serializer.data}')
      else:
        res = False
        print(f'failed update {student_serializer.data}')
        return res
  res = True
  return res

def addSubjectClasstoDF(thisdict, subject_id):
  for i in thisdict:
    if subject_id in thisdict[i]:
      return i
  return 'อื่นๆ'


@csrf_exempt
def addSubject(df, thisdict):
    df['subject_key'] = df['subject_key'].fillna('อื่นๆ')
    for index, subject in df.iterrows():
        subject_class = addSubjectClasstoDF(thisdict, subject['subject_id'])
        dic = {
            "subject_id": subject['subject_id'],
            "subject_name_thai": subject['subject_name_thai'],
            "subject_name_eng": subject['subject_name_eng'],
            "abstract": subject['abstract'],
            "subject_key": subject['subject_key'],
            "year": subject['year'],
            "subject_class": subject_class
        }
        this_subject = list(Subject_Data.objects.filter(
            subject_id=subject['subject_id'], subject_name_thai=subject['subject_name_thai'], subject_name_eng=subject['subject_name_eng'], year=subject['year']).values())
        if this_subject == []:
            subject_serializer = SubjectSerializer(data=dic)
            if subject_serializer.is_valid():
                subject_serializer.save()
                print(f'save {subject_serializer.data}')
            else:
                res = False
                print("Failed to add")
                return res
        else:
            this_subject = Subject_Data.objects.get(
                subject_id=subject['subject_id'], subject_name_thai=subject['subject_name_thai'], subject_name_eng=subject['subject_name_eng'])
            subject_serializer = SubjectSerializer(this_subject, data=dic)
            if subject_serializer.is_valid():
                subject_serializer.save()
                print(f'Update {subject_serializer.data}')
            else:
                res = False
                print("Failed to add")
                return res
    res = True
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
  grade_map = {
      "A": 4.00,
      "S": 4.00,
      "T(S)": 4.00,
      "T(A)": 4.00,
      "B+": 3.50,
      "T(B+)": 3.50,
      "B": 3.00,
      "T(B)": 3.00,
      "C+": 2.50,
      "T(C+)": 2.50,
      "C": 2.00,
      "T(C)": 2.00,
      "D+": 1.50,
      "T(D+)": 1.50,
      "D": 1.00,
      "T(D)": 1.00,
      "F": 0.00,
      "T(F)": 0.00,
      "U": 0.00,
      "I": 0.00,
  }
  df["grade"] = df["grade"].replace(grade_map)
  return df



def transfromAlldfs(dfs):
  for i in dfs:
    dfs[i][0] = transfromGrade(dfs[i][0])
  return dfs


##### This Funtion Generate A thisdict item that consit of a {class: [subid,...,subid]} For a use in reqPredperUser ######
def genSubjectDict(df):
  thisdict = {}
  for index, row in df.iterrows():
    lisKeys = list(thisdict.keys())
    subId = row['subject_id']
    subClass = row['subject_class']
    if lisKeys == [] or subClass not in lisKeys:
      d = {subClass:[]}
      d[subClass].append(subId)
      thisdict.update(d)
    else:
      thisdict[subClass].append(subId)
  return thisdict


def findSubjectClass(subId, thisdict):
  for i in thisdict:
    if subId in thisdict[i]:
      return i
  return "อื่นๆ"




def train_rec_model(df):
  min_rating = 0.00
  max_rating = 4.00
  reader = Reader(rating_scale=(min_rating, max_rating))
  param_grid = {
        'n_factors': [20, 50, 100],
        'n_epochs': [5, 10, 20]
        }
  data = Dataset.load_from_df(df[['student_id', 'subject_id', 'grade']], reader)
  svd = SVD(n_epochs=10)
  gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=10)
  gs.fit(data)
  best_factor = gs.best_params['rmse']['n_factors']
  best_epoch = gs.best_params['rmse']['n_epochs']
  trainset, testset = train_test_split(data, test_size=.10, random_state=42)
  svd = gs.best_estimator["rmse"]
  svd.fit(trainset)
  pred_model = svd.test(testset)
  model = {
    "rmse" : round(accuracy.rmse(pred_model, verbose=True), 4),
    "model" : svd
  }
  return model

def train_sim_model_career(df):
  min_rating = 0.00
  max_rating = 4.00
  reader = Reader(rating_scale=(min_rating, max_rating))
  param_grid = {
        'n_factors': [20, 50, 100],
        'n_epochs': [5, 10, 20]
        }
  data = Dataset.load_from_df(df[['student_id', 'subject_class', 'grade']], reader)
  svd = SVD(n_epochs=10)
  gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=10)
  gs.fit(data)
  best_factor = gs.best_params['rmse']['n_factors']
  best_epoch = gs.best_params['rmse']['n_epochs']
  trainset, testset = train_test_split(data, test_size=.10, random_state=42)
  svd = gs.best_estimator["rmse"]
  svd.fit(trainset)
  pred_model = svd.test(testset)
  model = {
    "rmse" : round(accuracy.rmse(pred_model, verbose=True), 4),
    "model" : svd
  }
  return model


def generate_data_set(curriculum, year):
  curri_year = int(year)
  while curri_year % 4 != 0:
    curri_year = curri_year - 1
  curri_year = str(curri_year)
  s_data = pd.DataFrame(list(Student_Data.objects.all().values()))
  s_grade = pd.DataFrame(list(Student_Grade.objects.all().values()))
  sub_data = list(Subject_Data.objects.filter(year = curri_year).values())
  sub_data_df = pd.DataFrame(sub_data)
  join_q = "select s_grade.student_id, s_grade.subject_id, s_grade.grade, s_data.career, s_data.curriculum, s_data.status, s_data.curriculum_year from s_grade left join s_data on s_grade.student_id = s_data.student_id where s_grade.subject_id NOT LIKE '90%'"
  train_data = sqldf(join_q)
  join_q_sub = "select train_data.student_id, train_data.subject_id, train_data.grade, train_data.career, train_data.curriculum, train_data.status, train_data.curriculum_year, sub_data_df.subject_class from train_data left join sub_data_df on train_data.subject_id = sub_data_df.subject_id"
  train_data = sqldf(join_q_sub)
  train_data = train_data.loc[(train_data['grade'] != 'Zero') & (train_data['grade'] != 'nan') & (train_data['curriculum'] == curriculum) & (train_data['status'] == 'graduate') & (train_data['curriculum_year'] == curri_year)]
  train_data['subject_class'] = train_data['subject_class'].fillna('อื่นๆ')
  train_data = transfromGrade(train_data)
  return train_data


def prediction_grade_user(model, student_id, selected_values):
  predict_result = []
  for i in selected_values:
    d = {
      "subject_id": i,
      "grade": model.predict(str(student_id), str(i)).est
    }
    predict_result.append(d)
  return predict_result


def create_data_set_for_career(model, student_id, df, u_sub, job):
   subject_ids_student = df.loc[df["student_id"] == student_id, "subject_class"]
   print(subject_ids_student)
   subject_ids_to_pred = np.setdiff1d(u_sub, subject_ids_student)
   print(subject_ids_to_pred)
   df = pd.DataFrame(columns=['student_id', 'subject_class', 'grade', 'career'])
   for i in subject_ids_to_pred:
     df1 = pd.DataFrame([{'student_id': student_id, 'subject_class': i, 'grade': round(model.predict(str(student_id), str(i)).est, 2), 'career': job}])
     df = pd.concat([df, df1])
   return df


def transpost_df(df):
  lis_of_subClass = list(df['subject_id'].unique())
  lis_of_student = list(df['student_id'].unique())
  sub = 0
  int_class = []
  for sub in range(len(lis_of_subClass)):
    int_class.append(int(lis_of_subClass[sub]))
  lis_of_subClass = sorted(int_class)
  col = ['student_id']
  col = col + lis_of_subClass
  col.append('career')
  df_for_job = pd.DataFrame(columns=col)
  for i in lis_of_student:
    df_for_id = df[df.student_id == i]
    mini_row = {'student_id' : i}
    grade_dic = {}
    for index, row in df_for_id.iterrows():
      stu_job = {'career' : row['career']}
      grade = {int(row['subject_id']) : row['grade']}
      grade_dic.update(grade)
    grade_dic = dict(sorted(grade_dic.items()))
    grade_dic.update(stu_job)
    mini_row.update(grade_dic)
    df_for_job = df_for_job.append(mini_row, ignore_index=True)
  return df_for_job



def train_career_model(df):
  param_grid = {
    'n_estimators': [50],
    'max_features': ['log2'],
    'max_depth': [10],
    'min_samples_split': [5],
    'min_samples_leaf': [1, 2, 4]
  }
  rf = RandomForestClassifier()
  grid_search = gd_career(estimator=rf, param_grid=param_grid, cv=5)
  df_for_career = df
  y = df_for_career['career']
  X = df_for_career.drop('career', axis=1)
  X_train, X_test, y_train, y_test = tt_split(X, y, test_size=0.1, random_state = 42)
  grid_search.fit(X_train, y_train)
  best_rf = RandomForestClassifier(n_estimators=grid_search.best_params_['n_estimators'], 
                                 max_features=grid_search.best_params_['max_features'],
                                 max_depth=grid_search.best_params_['max_depth'],
                                 min_samples_split=grid_search.best_params_['min_samples_split'],
                                 min_samples_leaf=grid_search.best_params_['min_samples_leaf'])
  best_rf.fit(X_train, y_train)
  y_pred = best_rf.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  dataset_cols = X.columns.to_list()
  model = {
    "accuracy" : round(accuracy, 2),
    "model" : best_rf,
    "train_set_cols": dataset_cols
  }
  return model




@csrf_exempt
def create_career_model(request, name = 'Model_career', curriculum = 'วิศวกรรมคอมพิวเตอร์', year = '2562'):
  if request.method == 'POST':
    if request.body:
      body = json.loads(request.body)
      name = body['name']
      curriculum = body['curriculum']
      year = body['year']
    pre_avg_data = generate_data_set(curriculum, year)
    this_model_curri_year = pre_avg_data.loc[0, "curriculum_year"]
    trans_df = transpost_df(pre_avg_data)
    trans_df = trans_df.fillna(99)
    trans_df = trans_df[trans_df["career"] != 'Zero']
    job = trans_df['career']
    trans_df = trans_df.drop('student_id', axis=1)
    trans_df = trans_df.drop('career', axis=1)
    trans_df = trans_df.astype(float)
    trans_df['career'] = job.to_list() 
    try:
      career_model = train_career_model(trans_df)
    except:
      res = {"message" : "Error in model training process", "status" : status.HTTP_400_BAD_REQUEST}
      return JsonResponse(res, safe=False)
    print(career_model)
    career_model = CareerModel(name = name, curriculum = curriculum, year = this_model_curri_year, accuracy = career_model['accuracy'], train_set_cols = career_model['train_set_cols'],career_model = career_model['model'])
    career_model.save()
    res = {"message": f'Complete creating career model name : {name} curriculum : {curriculum}'}
  else:
    res = {"message": "Method not match.", "status": status.HTTP_400_BAD_REQUEST}
  return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})



def reqPredictPerUser_Production(df_user, student_id = 'Optional', curriculum = 'วิศวกรรมคอมพิวเตอร์', year = '2562'):
    curri_year = int(year)
    while curri_year % 4 != 0:
      curri_year = curri_year - 1
    curri_year = str(curri_year)
    sub_data = list(Subject_Data.objects.filter(year = curri_year).values())
    sub_data_df = pd.DataFrame(sub_data)
    all_career_model = list(CareerModel.objects.filter(curriculum = curriculum).values()) ##
    all_career_model = all_career_model[-1] ##
    career_model = all_career_model['career_model']  ##
    train_set_cols = all_career_model['train_set_cols'] ##
    df_user = transfromGrade(df_user)
    main_data_set = generate_data_set(curriculum, year)
    selected_values = df_user.query("Want_To_Predict == '?'")['subject_id'].tolist()
    df_user = df_user[df_user.grade != 'Zero']
    df_user_career = df_user ##
    df_user_career['career'] = np.nan ##
    df_user_career['career'] = df_user_career['career'].fillna('Zero') ##
    user_sub = list(df_user_career['subject_id'].unique()) ##
    user_sub_int = [int(element) for element in user_sub] ##
    not_valid_sub = []
    for j in user_sub:
      if int(j) not in train_set_cols:
        not_valid_sub.append(j)
    for k in not_valid_sub:
      df_user_career = df_user_career[df_user_career['subject_id'] != k]
    ungrade_sub = list(set(train_set_cols)-set(user_sub_int))
    for i in ungrade_sub:
      new = pd.DataFrame({"student_id": ['Optional'],"subject_id": [i]})
      df_user_career = pd.concat([df_user_career, new], ignore_index=True)
    df_user_career = transpost_df(df_user_career) ##
    df_user_career = df_user_career ##
    df_user_career_for_test = df_user_career.drop(columns=['student_id','career']) ##
    df_user_career_for_test = df_user_career_for_test.fillna(99)
    df_user_career_for_test = df_user_career_for_test.astype(float)
    pred_result_career = career_model.predict(df_user_career_for_test)[0]
    subId_name = {row['subject_id']:row['subject_name_eng'] for row in Subject_Data.objects.values()}
    full_data_set_for_pred_grade = pd.concat([main_data_set, df_user], axis=0)
    model_grade_pred = train_rec_model(full_data_set_for_pred_grade)
    predictions = prediction_grade_user(model_grade_pred['model'], student_id, selected_values)
    response_grade = []
    for i in predictions:
        if i['subject_id'] in subId_name:
            dic = {"subject_id" : i['subject_id'], "sub_name" : subId_name[i['subject_id']], "grade" : round(i['grade'], 2)}
            response_grade.append(dic)
    response_grade.append(str(pred_result_career))
    return response_grade

@csrf_exempt
def generateRecModel_manyUser(request, name = 'Default', curriculum = 'วิศวกรรมคอมพิวเตอร์', curri_year = '2560'):
  if request.method == 'POST':
    if request.body:
      try:
        body = json.loads(request.body)
        curriculum = body['curriculum']
        curri_year = body['curri_year']
        name = body['name']
      except:
        pass
    student_data = pd.DataFrame(list(Student_Data.objects.all().values()))
    student_grade = pd.DataFrame(list(Student_Grade.objects.all().values()))
    student_grade = student_grade[student_grade['grade'] != 'Zero']
    student_grade = transfromGrade(student_grade)
    subject_data = pd.DataFrame(list(Subject_Data.objects.filter(year = curri_year).values()))
    q_join_grade = "select student_grade.student_id, student_grade.subject_id, student_grade.grade, student_data.curriculum, student_data.curriculum_year, student_data.career from student_grade left join student_data on student_grade.student_id = student_data.student_id"
    dataset = sqldf(q_join_grade)
    dataset = dataset.loc[(dataset['curriculum'] == curriculum) & (dataset['curriculum_year'] == curri_year)]
    q_join_subject = "select dataset.student_id, subject_data.subject_class, dataset.grade, dataset.curriculum, dataset.curriculum_year, dataset.career from dataset left join subject_data on dataset.subject_id = subject_data.subject_id"
    dataset = sqldf(q_join_subject)
    dataset = dataset[dataset['grade'] != 'nan']
    q_avg = "select dataset.student_id, dataset.subject_class, round(avg(dataset.grade),2) as grade, dataset.curriculum, dataset.curriculum_year, dataset.career from dataset group by dataset.subject_class, dataset.student_id"
    dataset = sqldf(q_avg)
    print(dataset['subject_class'].unique())
    dataset['subject_class'] = dataset['subject_class'].fillna('อื่นๆ')
    dataset = dataset[['student_id', 'subject_class', 'grade']]
    try:
      model_fill_grade = train_sim_model_career(dataset)
    except:
      res = {"message" : "Error in model training process", "status" : status.HTTP_400_BAD_REQUEST}
      return JsonResponse(res, safe=False)
    model_fill_grade = SurpriseModel(name = name, curriculum = curriculum, year = curri_year, rmse = model_fill_grade['rmse'], type_pred = 'Subject_Class', rec_model = model_fill_grade['model'])
    model_fill_grade.save()
    res = {"message" : f'Complete creating recomm model name : {name} | curriculum : {curriculum} | curri_year : {curri_year}'}
  else:
    res = {"message": "Method not match.", "status": status.HTTP_400_BAD_REQUEST}
  return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def reqPredict_career_manyUser(request, curriculum = 'วิศวกรรมคอมพิวเตอร์', start_year = '2562'):
  if request.method == 'POST':
    if request.body:
      try:
        body = json.loads(request.body)
        curriculum = body['curriculum']
        start_year = body['year']
      except:
        pass
    curri_year = int(start_year)
    while curri_year % 4 != 0:
      curri_year = curri_year - 1
    curri_year = str(curri_year)
    try:
      # model_rec = list(SurpriseModel.objects.filter(curriculum = curriculum, year = curri_year).values())[-1]
      model_career = list(CareerModel.objects.filter(curriculum = curriculum, year = curri_year).values())[-1]
    except:
      res = {"message" : "Can't find model that suite your request", "status" : status.HTTP_400_BAD_REQUEST}
      return JsonResponse(res, safe=False)
    train_set_cols = model_career['train_set_cols']
    career_model = model_career['career_model']
    s_data = pd.DataFrame(list(Student_Data.objects.all().values()))
    s_grade = pd.DataFrame(list(Student_Grade.objects.all().values()))
    join_q = "select s_grade.student_id, s_grade.subject_id, s_grade.grade, s_data.career, s_data.curriculum, s_data.status, s_data.curriculum_year, s_data.start_year from s_grade left join s_data on s_grade.student_id = s_data.student_id where s_grade.subject_id NOT LIKE '90%'"
    dataset = sqldf(join_q)
    dataset = dataset.loc[(dataset['grade'] != 'Zero') & (dataset['grade'] != 'nan') & (dataset['curriculum'] == curriculum) & (dataset['curriculum_year'] == curri_year)]
    dataset = dataset[dataset['start_year'] == start_year]
    dataset = dataset[dataset['career'] == 'Zero']
    unique_sub_by_year = [int(element) for element in list(dataset['subject_id'].unique())]
    for i in unique_sub_by_year:
      if i not in train_set_cols:
        if len(str(i)) == 7:
          a = '0' + str(i) 
        dataset = dataset[dataset['subject_id'] != a]
    unique_sub_by_year = [int(element) for element in list(dataset['subject_id'].unique())]
    un_assign_sub = list(set(train_set_cols) - set(unique_sub_by_year))
    dataset = dataset[['student_id', 'subject_id', 'grade', 'career']]
    dataset = transfromGrade(dataset)
    for i in un_assign_sub:
      new = pd.DataFrame({"student_id": ['temp'], "subject_id": [i]})
      dataset = pd.concat([dataset, new], ignore_index=True)
    dataset = transpost_df(dataset)
    dataset = dataset[dataset['student_id'] != 'temp']
    dataset = dataset.drop(columns=['student_id','career'])
    dataset = dataset.fillna(99)
    dataset = dataset.astype(float)
    # pred_result = career_model.predict(dataset)
    career_list = career_model.classes_
    pred_prob = career_model.predict_proba(dataset)
    pred_prob = pred_prob.tolist()
    career_counts = defaultdict(int)
    for prob in pred_prob:
      sub_career_dict = dict(zip(career_list, prob))
      sub_career_dict = dict(sorted(sub_career_dict.items(), key=lambda x: x[1], reverse=True))
      top_careers = list(sub_career_dict.keys())[:2]
      for career in top_careers:
        career_counts[career] += 1
    career_counts = dict(career_counts)
    response = {}
    lis_key = list(career_counts.keys())
    for car in lis_key:
      dic = {car : {"Year" : start_year, "Num_of_student" : career_counts[car]}}
      response.update(dic)
    # for j in pred_result:
    #   lis_key = list(response.keys())
    #   if j in lis_key:
    #     response[j]['Num_of_student'] += 1
    #   else:
    #     dic = {j : {"Year" : start_year, "Num_of_student" : 1}}
    #     response.update(dic)
    res = {"message" : response, "status" : status.HTTP_200_OK}
  else:
    res = {"message": "Method not match.", "status": status.HTTP_400_BAD_REQUEST}
  return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})


