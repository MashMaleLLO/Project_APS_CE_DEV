from asyncio import constants
from cgi import test
from pyexpat import model
from unittest.util import safe_repr
from urllib import response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Student_Data, Student_Grade,Subject_Data, SurpriseModel, CSV_File
from .serializers import StudentGradeSerializer, StudentSerializer, SubjectSerializer
from rest_framework.parsers import JSONParser
from django.db.models import Q
from datetime import date
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
from surprise.model_selection import train_test_split
from surprise.model_selection import GridSearchCV
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
        this_file = pd.DataFrame(this_file)
        res = this_file[['id','name', 'upload_date', 'update_date', 'del_flag', 'type_data']].to_dict('records')[0]
        res = { "message" : res, "status": status.HTTP_200_OK }
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
    for index,subject in df.iterrows():
        subject_class = addSubjectClasstoDF(thisdict, subject['subject_id'])
        dic = {
            "subject_id":subject['subject_id'],
            "subject_name_thai":subject['subject_name_thai'],
            "subject_name_eng":subject['subject_name_eng'],
            "abstract":subject['abstract'],
            "subject_key":subject['subject_key'],
            "year":subject['year'],
            "subject_class": subject_class
        }
        this_subject = Subject_Data.objects.get(subject_id = subject['subject_id'], subject_name_thai = subject['subject_name_thai'], subject_name_eng = subject['subject_name_eng'])
        if this_subject == None:
          subject_serializer = SubjectSerializer(data=dic)
          if subject_serializer.is_valid():
              subject_serializer.save()
              print(f'save {subject_serializer.data}')
          else:
              res = False
              print("Failed to add")
              return res
        else:
          subject_serializer = SubjectSerializer(this_subject,data=dic)
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



def addFullCSVtoDFS(dfs):
  allStudentIds = {}
  for i in dfs:
    stuid = list(dfs[i][1]['student_id'].unique())
    dic = {i:stuid}
    allStudentIds.update(dic)
  return allStudentIds



def generateFullCSVByClass(model, student_id, subject, df, curri, n_items):
    targetDF = df
    for i in student_id:
      subject_ids = df["subject_class"].unique()
      subject_ids_student = df.loc[df["student_id"] == i, "subject_class"]
      subject_ids_to_pred = np.setdiff1d(subject_ids, subject_ids_student)
      test_set = [[i, subject_id, 4] for subject_id in subject_ids_to_pred]
      predictions = model.test(test_set)
      pred_ratings = np.array([pred.est for pred in predictions])
      index_max = (-pred_ratings).argsort()[:n_items]
      for j in index_max:
       subject_id = subject_ids_to_pred[j]
       targetDF = pd.concat([targetDF, pd.DataFrame.from_records([{'student_id' : i, 'grade' : round(pred_ratings[j], 2), 'semester' : 'prediction', 'year' : 'prediction', 'curriculum' : curri, 'subject_class' : subject_id}])], ignore_index=True)
    return targetDF



def generateFullCSVByGrade(model, student_id, subject, df, curri, n_items):
    targetDF = df
    subject_ids = df["subject_id"].unique()
    subject_ids_student = df.loc[df["student_id"] == student_id, "subject_id"]
    subject_ids_to_pred = np.setdiff1d(subject_ids, subject_ids_student)
    test_set = [[student_id, subject_id, 3] for subject_id in subject_ids_to_pred]
    predictions = model.test(test_set)
    pred_ratings = np.array([pred.est for pred in predictions])
    index_max = (-pred_ratings).argsort()[:n_items]
    for j in index_max:
      subject_id = subject_ids_to_pred[j]
      targetDF = pd.concat([targetDF, pd.DataFrame.from_records([{'student_id' : student_id, 'subject_id' : subject_id,'grade' : round(pred_ratings[j], 2), 'semester' : 'prediction', 'year' : 'prediction', 'curriculum' : curri}])], ignore_index=True)
    return targetDF



def passDFStoFunc(dfs, student_id_lis, thisdict, byWhat):
  for i in dfs:
    stuID = student_id_lis[i]
    model = dfs[i][2]
    data = dfs[i][1]
    curri = i
    NumOfSub = len(list(thisdict.keys()))
    if byWhat == 0:
      final_df = generateFullCSVByGrade(model, stuID, 'sub', data, curri, NumOfSub)
    else:
      final_df = generateFullCSVByClass(model, stuID, 'sub', data, curri, NumOfSub)
    q_sort = "SELECT * FROM final_df ORDER BY student_id"
    final_df = sqldf(q_sort)
    dfs[i].append(final_df)
  return dfs


@csrf_exempt
def train_rec_model(df, mode = 0):
  min_rating = 0.00
  max_rating = 4.00
  reader = Reader(rating_scale=(min_rating, max_rating))
  param_grid = {
        'n_factors': [20, 50, 100],
        'n_epochs': [5, 10, 20]
        }
  if mode == 0:
    data = Dataset.load_from_df(df[['student_id', 'subject_class', 'grade']], reader)
  else:
    data = Dataset.load_from_df(df[['student_id', 'subject_id', 'grade']], reader)
  svd = SVD(n_epochs=10)
  gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=10)
  gs.fit(data)
  best_factor = gs.best_params['rmse']['n_factors']
  best_epoch = gs.best_params['rmse']['n_epochs']
  trainset, testset = train_test_split(data, test_size=.10)
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
  if request.method == 'POST':
    if request.body:
      body = json.loads(request.body)
      model_name = body['name']
      model_year = body['year']
      model_type = body['type']
      model_curri = body['curriculum']
      curri_year = int(model_year)
      while curri_year % 4 != 0:
        curri_year = curri_year - 1
      curri_year = str(curri_year)
      s_data = pd.DataFrame(list(Student_Data.objects.all().values()))
      s_grade = pd.DataFrame(list(Student_Grade.objects.all().values()))
      sub_data = list(Subject_Data.objects.filter(year = curri_year).values())
      sub_data_df = pd.DataFrame(sub_data)
      thisdict = genSubjectDict(sub_data_df)
      join_q = "select s_grade.student_id, s_grade.subject_id, s_grade.grade, s_data.career, s_data.curriculum, s_data.status, s_data.curriculum_year from s_grade left join s_data on s_grade.student_id = s_data.student_id where s_grade.subject_id NOT LIKE '90%'"
      train_data = sqldf(join_q)
      train_data = train_data.loc[(train_data['grade'] != 'Zero') & (train_data['grade'] != 'nan') & (train_data['curriculum'] == model_curri) & (train_data['status'] == 'graduate') & (train_data['curriculum_year'] == curri_year)]
      train_data = transfromGrade(train_data)
      if model_type == 'class':
        train_data['subject_class'] = train_data.apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
        group_query = "select student_id, subject_class, round(avg(grade), 2) as grade from train_data group by subject_class, student_id order by student_id"
        train_data = sqldf(group_query)
        return_model = train_rec_model(train_data)
      else:
        return_model = train_rec_model(train_data,1)
      this_rmse = str(return_model['rmse'])
      rec = SurpriseModel(name = model_name, curriculum = model_curri, rmse = this_rmse, type_pred = model_type, rec_model = return_model['model'])
      rec.save()
      res = {"message": f'Model successfuly create name : {model_name} for : {model_curri} type : {model_type} with rmse : {this_rmse}.', "status" : status.HTTP_200_OK}
    else:
      res = {"message": "Pls select model type and curriculum", "status": status.HTTP_400_BAD_REQUEST}
  else:
    res = {"message": "Method not match.", "status": status.HTTP_400_BAD_REQUEST}
  return JsonResponse(res , safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def reqPredictPerUser(df_user, model_id):
  ##### Get Curriculum From User #####
  this_user_curri = df_user.loc[0,'curriculum']
  ##### Find Model By It ID #####
  all_models = list(SurpriseModel.objects.all().values())
  model = "NOTFOUND"
  model_type = "NOTFOUND"
  for i in all_models:
    if str(i['id']) == model_id:
      model = i['args']['model']
      model_type = i['args']['type']
  print(model)
  ###############################
  response = []
  q_subject_data = list(Subject_Data.objects.all().values())
  df_subject = pd.DataFrame(q_subject_data)
  ##### Create A Suject Dict {ID:NAME} #####
  subId_name = {}
  for index_sub, row_sub in df_subject.iterrows():
    dic_sub = {row_sub['subject_id']:row_sub['subject_name_eng']}
    subId_name.update(dic_sub)
  # print(subId_name)
  ##########################################
  thisdict = genSubjectDict(df_subject)
  df_user = transfromGrade(df_user)
  df_user = df_user[df_user.grade != 'Zero']
  qdata = list(Student.objects.filter(curriculum='วิศวกรรมคอมพิวเตอร์').values())
  df = pd.DataFrame(qdata)
  df = transfromGrade(df)
  dfs = []
  copy_origin_df = df
  non_Zero_df = copy_origin_df[copy_origin_df.grade != 'Zero']
  dfs.append(df)
  dfs.append(non_Zero_df)
  if model_type == 'Class':
    tempAVG = dfs[1]
    tempAVG_user = df_user 
    df_user['subject_class'] = df.apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
    dfs[1]['subject_class'] = dfs[1].apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
    q_find_AVG = "SELECT student_id, AVG(grade) as grade, semester, year, curriculum, subject_class FROM tempAVG GROUP BY subject_class, student_id ORDER BY student_id"
    q_find_AVG_user = "SELECT student_id, AVG(grade) as grade, semester, year, curriculum, subject_class FROM tempAVG_user GROUP BY subject_class, student_id ORDER BY student_id"
    tempDFS_AVG = sqldf(q_find_AVG)
    tempDF_AVG_USER = sqldf(q_find_AVG_user)
    dfs[1] = tempDFS_AVG
    df_user = tempDF_AVG_USER 
    # model_file = joblib.load('recommend/ML_model/Class_test_New_01_วิศวกรรมคอมพิวเตอร์.pkl')
    subject_id_in_dataset = dfs[1]['subject_class'].unique()
    subject_id = df_user['subject_class']
  else:
    # model_file = joblib.load('recommend/ML_model/Grade_test_New_01_วิศวกรรมคอมพิวเตอร์.pkl')
    subject_id_in_dataset = dfs[1]['subject_id'].unique()
    subject_id = df_user['subject_id']
  subject_ids_to_pred = np.setdiff1d(subject_id_in_dataset, subject_id)
  test_set = [['Optional', sub, 4] for sub in subject_ids_to_pred]
  # model_file = all_models[-1]['args']['model']
  # model_file = cPickle.loads(model_file)
  predictions = model.test(test_set)
  pred_ratings = np.array([pred.est for pred in predictions])
  NumOfSub = len(subject_id_in_dataset)
  index_max = (-pred_ratings).argsort()[:NumOfSub]
  for j in index_max:
    sub = subject_ids_to_pred[j]
    if model_type == 'Grade':
      lisForFindSubId = list(subId_name.keys())
      if sub in lisForFindSubId:
        dic = {"subject_id" : sub, "sub_name" : subId_name[sub], "grade" : round(pred_ratings[j], 2)}
      else:
        dic = {"subject_id" : sub, "sub_name" : "ไม่พบวิชาในฐานข้อมูล", "grade" : round(pred_ratings[j], 2)}
    else:
      dic = {"subject_class" : sub, "subject_in_class": thisdict[sub],"grade" : round(pred_ratings[j], 2)}
    response.append(dic)
  return response



def reqPredictPerUser_Production(df_user):    
    all_models = list(SurpriseModel.objects.all().values())
    model = None
    for i in all_models:
        if str(i['id']) == '1':
            model = i['rec_model']
            model_type = i['type_pred']
    if model is None:
        print("Model not found")
        return
    df_user = transfromGrade(df_user)
    selected_values = df_user.query("Want_To_Predict == '?'")['subject_id'].tolist()
    df_user = df_user[df_user.grade != 'Zero']
    graded_sub = df_user['subject_id'].tolist()
    subId_name = {row['subject_id']:row['subject_name_eng'] for row in Subject_Data.objects.values()}
    subject_ids_to_pred = selected_values
    test_set = []
    for sub in graded_sub:
      this_sub_grade = df_user.loc[df_user['subject_id'] == sub, 'grade'].iloc[0]
      test_set.append(['Optional', sub, this_sub_grade])
    for sub in selected_values:
      grade = None
      test_set.append(['Optional', sub, this_sub_grade])
    print(test_set)
    predictions = model.test(test_set)
    pred_ratings = [pred.est for pred in predictions]
    pred_ratings = [(subject_ids_to_pred[i], pred_ratings[i]) for i in range(len(subject_ids_to_pred))]
    pred_ratings.sort(key=lambda x: x[1], reverse=True)
    response = []
    for sub_id, grade in pred_ratings:
        if sub_id in subId_name:
            dic = {"subject_id" : sub_id, "sub_name" : subId_name[sub_id], "grade" : round(grade, 2)}
            response.append(dic)
    return response
