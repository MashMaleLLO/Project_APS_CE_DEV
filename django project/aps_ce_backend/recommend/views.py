from pyexpat import model
from urllib import response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Student, Subject_Data, SurpriseModel
from .serializers import StudentSerializer, SubjectSerializer
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
from surprise import SVD
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split
from surprise.model_selection import GridSearchCV
import numpy as np

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
            return JsonResponse(student_serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def subjectApi(requset,id=0):
  if requset.method == 'GET':
    print(id)
    if id == 0:
      subjects = Subject_Data.objects.all()
      subjects_serializer = SubjectSerializer(subjects, many=True)
      return JsonResponse(subjects_serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
      subject = Subject_Data.objects.get(subject_id = id)
      subject_serializer = SubjectSerializer(subject)
      return JsonResponse(subject_serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})



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
        subject_serializer = SubjectSerializer(data=dic)
        if subject_serializer.is_valid():
            subject_serializer.save()
            print(f'save {subject_serializer.data}')
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
def generateModel(request, curri):
    if request.method == 'POST':
      body_unicode = request.body
      body = json.loads(body_unicode)
      model_name = body['name']
      model_pred = body['pred']
      print(model_pred)
      qdata = list(Student.objects.all().values())
      q_subject_data = list(Subject_Data.objects.all().values())
      df_subject = pd.DataFrame(q_subject_data)
      thisdict = genSubjectDict(df_subject)
      df = pd.DataFrame(qdata)
      dfs = queryBycurriculum(df)
      dfs = transfromAlldfs(dfs)
      for i in dfs:
        temp = dfs[i][0]
        temp = temp[temp.grade != 'Zero']
        dfs[i].append(temp)
      # q_subjectClassAndsubId = 'SELECT subject_id, subject_class from df_subject;'
      # df_subject = sqldf(q_subjectClassAndsubId)
      if model_pred == 'Class':
        for j in dfs:
          dfs[j][0]['subject_class'] = dfs[j][0].apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
          dfs[j][1]['subject_class'] = dfs[j][1].apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
          # casttemp = dfs[j][1]
          # casttemp[["grade"]] = casttemp[["grade"]].apply(pd.to_numeric)
          # dfs[j][1] = casttemp
        for k in dfs:
          tempAVG = dfs[k][1]
          q_find_AVG = "SELECT student_id, AVG(grade) as grade, semester, year, curriculum, subject_class FROM tempAVG GROUP BY subject_class, student_id ORDER BY student_id"
          tempDFS_AVG = sqldf(q_find_AVG)
          dfs[k][1] = tempDFS_AVG
      min_rating = 0
      max_rating = 4
      reader = Reader(rating_scale=(min_rating, max_rating))
      param_grid = {
        'n_factors': [20, 50, 100],
        'n_epochs': [5, 10, 20]
        }
      for i in dfs:
        if model_pred == 'Class':
          data = Dataset.load_from_df(dfs[i][1][['student_id', 'subject_class', 'grade']], reader)
        else:
          data = Dataset.load_from_df(dfs[i][1][['student_id', 'subject_id', 'grade']], reader)
        svd = SVD(n_epochs=10)
        results = cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=10, verbose=True)
        gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=10)
        gs.fit(data)
        best_factor = gs.best_params['rmse']['n_factors']
        best_epoch = gs.best_params['rmse']['n_epochs']
        trainset, testset = train_test_split(data, test_size=.20)
        svd = SVD(n_factors=best_factor, n_epochs=best_epoch)
        svd.fit(trainset)
        print(gs.best_score['rmse'])
        dfs[i].append(svd)
        dfs[i].append(gs.best_score['rmse'])
      if curri == 'Com':
        curri = 'วิศวกรรมคอมพิวเตอร์'
        model_curri = str(curri)
        model_rmse = str(dfs[curri][3])
        model_type = str(body['pred'])
        model_file = dfs[curri][2]
        sur = SurpriseModel(args={'name': model_name, 'curriculum' : model_curri, 'type': model_type,'rmse': model_rmse, 'model': model_file})
        sur.save()
        # with open(f'recommend/ML_model/{model_type}_{model_name}_{model_curri}.pkl', 'wb') as fp:
        #   joblib.dump(dfs[curri][2],fp)
      else:
        curri = 'วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)'
        model_curri = str(curri)
        model_rmse = str(dfs[curri][3])
        model_type = str(body['pred'])
        model_file = cPickle.dumps(dfs[curri][2])
        # sur = SurpriseModel(args={'name': model_name, 'curriculum' : model_curri, 'type': model_type,'rmse': model_rmse, 'model': model_file})
        # sur.save()
        with open(f'recommend/ML_model/{model_type}_{model_name}_{model_curri}.pkl', 'wb') as fp:
          joblib.dump(dfs[curri][2],fp)
      return JsonResponse("Hi" , safe=False, json_dumps_params={'ensure_ascii': False})
    else:
      return JsonResponse("BAD REQUEST" , safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def reqPredictPerUser(df_user, model_id):
  all_models = list(SurpriseModel.objects.all().values())
  model = "NOTFOUND"
  model_type = "NOTFOUND"
  for i in all_models:
    if str(i['id']) == model_id:
      model = i['args']['model']
      model_type = i['args']['type']
  print(model)
  response = []
  q_subject_data = list(Subject_Data.objects.all().values())
  df_subject = pd.DataFrame(q_subject_data)
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
      dic = {"subject_id" : sub, "grade" : round(pred_ratings[j], 2)}
    else:
      dic = {"subject_class" : sub, "grade" : round(pred_ratings[j], 2)}
    response.append(dic)
  return response