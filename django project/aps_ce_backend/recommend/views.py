from urllib import response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Student, Subject_Data
from .serializers import StudentSerializer, SubjectSerializer
# Create your views here.



import re
import requests
import pandas as pd
from pandasql import sqldf


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



def generateFullCSV(model, student_id, subject, df, curri, n_items):
    # targetDF = df_for_Com_Train_AVG
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

def passDFStoFunc(dfs, student_id_lis, thisdict):
  for i in dfs:
    stuID = student_id_lis[i]
    model = dfs[i][2]
    data = dfs[i][1]
    curri = i
    NumOfSub = len(list(thisdict.keys()))
    final_df = generateFullCSV(model, stuID, 'sub', data, curri, NumOfSub)
    q_sort = "SELECT * FROM final_df ORDER BY student_id"
    final_df = sqldf(q_sort)
    dfs[i].append(final_df)
  return dfs



@csrf_exempt
def generateModel(request):
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
    for j in dfs:
      dfs[j][0]['subject_class'] = dfs[j][0].apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
      dfs[j][1]['subject_class'] = dfs[j][0].apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
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
      data = Dataset.load_from_df(dfs[i][1][['student_id', 'subject_class', 'grade']], reader)
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
    student_id_lis = addFullCSVtoDFS(dfs)
    dfs = passDFStoFunc(dfs, student_id_lis, thisdict)
    # testDDDDD = dfs["วิศวกรรมคอมพิวเตอร์"][3].head()
    print(dfs["วิศวกรรมคอมพิวเตอร์"][3]['subject_class'].unique())
    return JsonResponse("Hi" , safe=False, json_dumps_params={'ensure_ascii': False})


def generatePredictionForUser(df_user):
    response = []
    q_find_non_grade = "SELECT * FROM df_user where grade = 'Zero'"
    user_id = "'" + str(df_user['student_id'].unique()[0]) + "'"
    user_curri = df_user['curriculum'].unique()[0]
    df_user_non_grade = sqldf(q_find_non_grade)
    non_grade_sub = list(df_user_non_grade['subject_id'].unique())
    qdata = list(Student.objects.all().values())
    q_subject_data = list(Subject_Data.objects.all().values())
    df_subject = pd.DataFrame(q_subject_data)
    thisdict = genSubjectDict(df_subject)
    df = pd.DataFrame(qdata)
    df = pd.concat([df, df_user], ignore_index=True)
    dfs = queryBycurriculum(df)
    dfs = transfromAlldfs(dfs)
    for i in dfs:
      temp = dfs[i][0]
      temp = temp[temp.grade != 'Zero']
      dfs[i].append(temp)
    for j in dfs:
      dfs[j][0]['subject_class'] = dfs[j][0].apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
      dfs[j][1]['subject_class'] = dfs[j][0].apply (lambda row: findSubjectClass(row['subject_id'], thisdict), axis=1)
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
      data = Dataset.load_from_df(dfs[i][1][['student_id', 'subject_class', 'grade']], reader)
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
    student_id_lis = addFullCSVtoDFS(dfs)
    dfs = passDFStoFunc(dfs, student_id_lis, thisdict)
    return_dfs = dfs[user_curri][3]
    p_for_string = "'" + 'prediction' + "'"
    q_find_predict_grade_user = f'SELECT student_id, grade, subject_class from return_dfs where student_id = {user_id} and semester = {p_for_string}'
    return_dfs = sqldf(q_find_predict_grade_user)
    for index_user, row_user in return_dfs.iterrows():
      user_subject_class = row_user['subject_class']
      if user_subject_class == "อื่นๆ":
        dic = {
          "subject_class":user_subject_class,
          "grade":row_user['grade']
        }
      else:
        dic = {
          "subject_class":user_subject_class,
          "subject_in_class": thisdict[user_subject_class],
          "grade":row_user['grade']
        }
      response.append(dic)
    return response

        

