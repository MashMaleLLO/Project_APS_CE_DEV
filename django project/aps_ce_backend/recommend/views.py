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
        res = this_file[['id','name', 'upload_date', 'update_date', 'del_flag', 'type_data']].to_dict('records')[0]
        res = { "message" : {"file_information" : res, "file_content" : content}, "status": status.HTTP_200_OK }
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


@csrf_exempt
def generate_rec_model(request):
  res = {"message": "Method not match.", "status": status.HTTP_400_BAD_REQUEST}
  return JsonResponse(res , safe=False, json_dumps_params={'ensure_ascii': False})


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
     df1 = pd.DataFrame([{'student_id': student_id, 'subject_class': i, 'grade': str(round(model.predict(str(student_id), str(i)).est, 2)), 'career': job}])
     df = pd.concat([df, df1])
   return df


def transpost_df(df):
  lis_of_subClass = list(df['subject_class'].unique())
  lis_of_student = list(df['student_id'].unique())
  sub = 0
  int_class = []
  for sub in range(len(lis_of_subClass)):
    if lis_of_subClass[sub] == 'อื่นๆ':
      pass
    else:
      int_class.append(int(lis_of_subClass[sub]))
  int_class = sorted(int_class)
  int_class.append('อื่นๆ')
  lis_of_subClass = int_class
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
      if row['subject_class'] == 'อื่นๆ': 
        un_int_class = {row['subject_class'] : row['grade']}
      else:  
        grade = {int(row['subject_class']) : row['grade']}
        grade_dic.update(grade)
    grade_dic = dict(sorted(grade_dic.items()))
    grade_dic.update(un_int_class)
    grade_dic.update(stu_job)
    mini_row.update(grade_dic)
    df_for_job = df_for_job.append(mini_row, ignore_index=True)
  temp_df = df_for_job
  df_for_job_train = temp_df.dropna()
  return df_for_job_train



def train_career_model(df):
  knn = KNeighborsClassifier()
  params = {'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance']}
  kfold = KFold(n_splits=5, shuffle=True, random_state=42)
  grid_search = gd_career(estimator=knn, param_grid=params, cv=kfold)
  le = preprocessing.LabelEncoder()
  y = df['career']
  y = le.fit_transform(y)
  print(y)
  y_ins = le.inverse_transform(y)
  print(y_ins)
  encode_dic = {}
  for i in range(len(y)):
    dic = {y[i]:y_ins[i]}
    encode_dic.update(dic)
  X = df.drop(columns=['student_id','career'])
  X_train, X_test, y_train, y_test = tt_split(X, y, test_size=0.1, random_state = 42)
  grid_search.fit(X_train, y_train)
  best_knn = KNeighborsClassifier(n_neighbors=grid_search.best_params_['n_neighbors'], 
                                 weights=grid_search.best_params_['weights'])
  best_knn.fit(X_train, y_train)
  test_score = best_knn.score(X_test, y_test)
  accuracy = test_score
  model = {
    "accuracy" : round(accuracy, 2),
    "model" : best_knn,
    "encode_dict": encode_dic
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
    group_query = "select student_id, subject_class, round(avg(grade), 2) as grade, career from pre_avg_data group by subject_class, student_id order by student_id"
    avg_data = sqldf(group_query)
    model_career = train_sim_model_career(avg_data)
    subject_id_uni = avg_data["subject_class"].unique().tolist()
    student_id_uni = avg_data['student_id'].unique().tolist()
    final_df = pd.DataFrame(columns=['student_id', 'subject_class', 'grade', 'career'])
    for i in student_id_uni:
      this_user_job = avg_data.loc[avg_data['student_id'] == i, 'career'].values[0]
      df_temp = create_data_set_for_career(model_career['model'], i, avg_data, subject_id_uni, this_user_job)
      final_df = pd.concat([final_df, df_temp])
    final_df = pd.concat([avg_data, final_df])
    trans_df = transpost_df(final_df)
    trans_df = trans_df[trans_df["career"] != 'Zero']
    career_model = train_career_model(trans_df)
    print(career_model)
    career_model = CareerModel(name = name, curriculum = curriculum, accuracy = career_model['accuracy'], encode_class = career_model['encode_dict'],career_model = career_model['model'])
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
    encode_class = all_career_model['encode_class'] ##
    df_user = transfromGrade(df_user)
    main_data_set = generate_data_set(curriculum, year)
    selected_values = df_user.query("Want_To_Predict == '?'")['subject_id'].tolist()
    df_user = df_user[df_user.grade != 'Zero']
    df_user_career = df_user ##
    df_user_career['career'] = np.nan ##
    df_user_career['career'] = df_user_career['career'].fillna('Zero') ##
    q_join_user_subclass = 'select df_user_career.student_id, sub_data_df.subject_class, round(avg(df_user_career.grade), 2) as grade, df_user_career.career from df_user_career left join sub_data_df on df_user_career.subject_id = sub_data_df.subject_id group by subject_class' ##
    df_user_career = sqldf(q_join_user_subclass) ##
    df_user_career['subject_class'] = df_user_career['subject_class'].fillna('อื่นๆ') ##
    group_query = "select student_id, subject_class, round(avg(grade), 2) as grade, career from main_data_set group by subject_class, student_id order by student_id" ##
    avg_data = sqldf(group_query) ##
    df_con_user_data_set = pd.concat([avg_data, df_user_career]) ##
    model_career_sim = train_sim_model_career(df_con_user_data_set) ##
    df_filtered_user = df_con_user_data_set[df_con_user_data_set['student_id'] == 'Optional'] ##
    subject_id_uni = df_con_user_data_set["subject_class"].unique().tolist() ##
    this_user_job = df_filtered_user.loc[df_filtered_user['student_id'] == student_id, 'career'].values[0] ##
    df_user_full_grade = create_data_set_for_career(model_career_sim['model'], student_id, df_con_user_data_set, subject_id_uni, this_user_job) ##
    df_user_full_grade = pd.concat([df_filtered_user, df_user_full_grade]) ##
    df_user_full_grade = transpost_df(df_user_full_grade) ##
    df_user_career_for_test = df_user_full_grade ##
    df_user_career_for_test = df_user_career_for_test.drop(columns=['student_id','career']) ##
    this_user_career = encode_class[int(career_model.predict(df_user_career_for_test)[0])] ##
    subId_name = {row['subject_id']:row['subject_name_eng'] for row in Subject_Data.objects.values()}
    full_data_set_for_pred_grade = pd.concat([main_data_set, df_user], axis=0)
    model_grade_pred = train_rec_model(full_data_set_for_pred_grade)
    predictions = prediction_grade_user(model_grade_pred['model'], student_id, selected_values)
    response_grade = []
    for i in predictions:
        if i['subject_id'] in subId_name:
            dic = {"subject_id" : i['subject_id'], "sub_name" : subId_name[i['subject_id']], "grade" : round(i['grade'], 2)}
            response_grade.append(dic)
    response_grade.append(str(this_user_career))
    return response_grade

@csrf_exempt
def generateRecModel_manyUser(request, curriculum = 'วิศวกรรมคอมพิวเตอร์', curri_year = '2560'):
  if request.method == 'POST':
    if request.body:
      try:
        body = json.loads(request.body)
        curriculum = body['curriculum']
        curri_year = body['curri_year']
      except:
        pass
    student_data = pd.DataFrame(list(Student_Data.objects.all().values()))
    student_grade = pd.DataFrame(list(Student_Grade.objects.all().values()))
    student_grade = student_grade[student_grade['grade'] != 'Zero']
    student_grade = transfromGrade(student_grade)
    subject_data = pd.DataFrame(list(Subject_Data.objects.all().values()))
    q_join_grade = "select student_grade.student_id, student_grade.subject_id, student_data.curriculum, student_data.curriculum_year from student_grade left join student_data on student_grade.student_id = student_data.student_id"
    dataset = sqldf(q_join_grade)
    q_join_subject = "select dataset.student_id, subject_data.subject_class, dataset.curriculum, dataset.curriculum_year from dataset left join subject_data on dataset.subject_id = subject_data.subject_id"
    dataset = sqldf(q_join_subject)
    # dataset = dataset.loc[dataset['grade'] != 'Zero']
    print(dataset['grade'].unique())
  else:
    res = {"message": "Method not match.", "status": status.HTTP_400_BAD_REQUEST}
  return JsonResponse("Hi", safe=False)

