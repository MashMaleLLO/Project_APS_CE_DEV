import re
from urllib import response
from django.http.response import JsonResponse
from django.http import HttpResponse
from recommend import views as recc
from recommend.models import Subject_Data, CSV_File, Rec_User
from recommend.serializers import StudentSerializer, SubjectSerializer, RecUSerializer
import pandas as pd
import csv
import codecs
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from pandasql import sqldf

import os
import gensim
import spacy
import en_core_web_sm
import nltk
import math
import pickle as cPickle
import json
from pytz import timezone
import pytz
from datetime import datetime
# nltk.download('stopwords')
from nltk.corpus import stopwords
# STOPWORDS = set(stopwords.words('english'))
# nlp = en_core_web_sm.load()

from rest_framework import generics, status, authentication, permissions
import jwt

def hello(requset):
    return JsonResponse("Hi", safe=False)

def Throw(request):
    a = recc.catch()
    return JsonResponse(a,safe=False)

@csrf_exempt
def student_grade_database_handler(request, csv_id = 2):
    df_lis = list(CSV_File.objects.all().values())
    df = None
    f_name = None
    for i in df_lis:
        if str(i['id']) == str(csv_id):
            df = i['file']
            f_name = i['name']
            df = cPickle.loads(df)
    if df is None:
        res = {'message':'error file not found', 'status': status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)
    df = df.astype(str)
    print(df)
    res_from_stu_grade = recc.addStudent_grade(df)
    res_from_stu_data = recc.addStudent_data(df)
    if res_from_stu_grade:
        res = {"message":f'Update file {f_name} Complete', "status": status.HTTP_200_OK}
        return JsonResponse(res, safe=False)
    else:
        res = {"message": f'Error occure : data {res_from_stu_data}, grade {res_from_stu_grade}', "status": status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)


@csrf_exempt
def update_career(request, csv_id = 3):
    df_lis = list(CSV_File.objects.all().values())
    df = None
    f_name = None
    for i in df_lis:
        if str(i['id']) == str(csv_id):
            df = i['file']
            f_name = i['name']
            df = cPickle.loads(df)
    if df is None:
        res = {'message':'error file not found', 'status': status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)
    df = df.astype(str)
    res_from_update_career = recc.career_update(df)
    if res_from_update_career:
        res = {"message":f'All career has been update by file : {f_name}', "status": status.HTTP_200_OK}
        return JsonResponse(res, safe=False)
    else:
        res = {"message":"Update failed", "status": status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)


@csrf_exempt
def subject_csv_upload_hander(request, csv_id = 4):
    df_lis = list(CSV_File.objects.all().values())
    df = None
    f_name = None
    for i in df_lis:
        if str(i['id']) == str(csv_id):
            df = i['file']
            f_name = i['name']
            df = cPickle.loads(df)
    if df is None:
        res = {'message':'error file not found', 'status': status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)
    df = df.astype(str)
    csvHandlerSubject(df)
    return None    


@csrf_exempt
def csv_upload(request, type_data='ข้อมูลรายวิชา'):
    if request.method == 'POST':
        csv_file = request.FILES['path_to_csv']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse("File format not match pls upload only .csv file", safe=False)
        df = pd.read_csv(csv_file, encoding='utf-8')
        print(df)
        df = df.astype(str) # cast all columns to str
        pickled_data = cPickle.dumps(df)
        if pickled_data:
            csv_m = CSV_File(name = csv_file.name, upload_date = datetime.now(pytz.timezone('Asia/Bangkok')), update_date = datetime.now(pytz.timezone('Asia/Bangkok')), del_flag = "0", type_data = type_data, file = pickled_data)
            csv_m.save()
            return JsonResponse(f'Upload file {csv_file.name} complete.', safe=False)
        else:
            return JsonResponse('serializer is not valid',safe=False)
    return JsonResponse('Method not match.', safe=False)


@csrf_exempt
def csvHandlerSubject(df):
    nltk.download('stopwords')
    STOPWORDS = set(stopwords.words('english'))
    nlp = en_core_web_sm.load()
    df_subject_pre_nlp = df
    for index, row in df_subject_pre_nlp.iterrows():
        strt = '0'
        subId = row['subject_id']
        if len(subId) < 8:
            strt += row['subject_id']
            subId = strt
        df_subject_pre_nlp.at[index, 'subject_id'] = subId
    df_subject_pre_nlp = df_subject_pre_nlp.drop_duplicates('subject_id', keep='first')
    df_subject_pre_nlp = df_subject_pre_nlp.reset_index()
    for sentence in df_subject_pre_nlp['abstract']:
        newsentence = sentence
        listnewsentence = []
        for i in newsentence.split():
            i = i.replace(';',"")
            i = i.replace(',',"")
            listnewsentence.append(i)
        newsentence = set(listnewsentence) - set(STOPWORDS)   
        newsentence = " ".join(list(newsentence))
        df_subject_pre_nlp = df_subject_pre_nlp.replace({'abstract': sentence}, {'abstract': newsentence}, regex=True)
    thisdict = {}
    all_docs = [nlp(row) for row in df_subject_pre_nlp['abstract']]
    num = 0
    for i in range(len(all_docs)):
        check = 0
        sims = []
        if list(thisdict.keys()) == []:
            thisdict[num] = [df_subject_pre_nlp.loc[df_subject_pre_nlp.index == i, 'subject_id'].iloc[0]]
            num += 1
        else:
            for x in thisdict:
                temp = df_subject_pre_nlp.loc[df_subject_pre_nlp['subject_id'] == thisdict[x][0], 'abstract'].iloc[0]
                sim = all_docs[i].similarity(nlp(temp))
                sims.append(sim)
            maxsim = max(sims)
            for x in thisdict:
                temp = df_subject_pre_nlp.loc[df_subject_pre_nlp['subject_id'] == thisdict[x][0], 'abstract'].iloc[0]
                sim = all_docs[i].similarity(nlp(temp))
                if sim >= 0.90 and sim == maxsim:
                    thisdict[x].append(df_subject_pre_nlp.loc[df_subject_pre_nlp.index == i, 'subject_id'].iloc[0])
                    check = 1
                    break
            if check != 1:
                thisdict[num] = [df_subject_pre_nlp.loc[df_subject_pre_nlp.index == i, 'subject_id'].iloc[0]]
                num += 1
    res = recc.addSubject(df_subject_pre_nlp, thisdict)
    return JsonResponse("Hi", safe=False)


def csvDownload(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Fname','Lname','Nname'])
    response['Content-Disposition'] = 'attachment; filename="APS_CE.csv"'
    return response

@csrf_exempt
def uc01_getGradResult(request, curri, year):
    if curri == "com":
        curri = "วิศวกรรมคอมพิวเตอร์"
    else:
        curri = "วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)"
    query = Q(curriculum = str(curri))
    query.add(Q(start_year = str(year)), Q.AND)
    students = list(Student.objects.filter(query).values())
    df = pd.DataFrame(students)
    query = "SELECT student_id, start_year, career, curriculum FROM df group by student_id"
    df = sqldf(query)
    students = df.values.tolist()
    if students != []:
        return JsonResponse(students , safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse("Can not Found any students" , safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def uc02_getPredResultByYear(request, curri, year):
    return 1

@csrf_exempt
def get_career_result(request):
    if request.method == 'GET':
        students = Student.objects.all()
        students = pd.DataFrame(list(students.values()))
        query = "select sub.career, sub.start_year, count(sub.student_id) as cnt_student from (select student_id, career, start_year from students where career <> 'Zero' group by student_id) as sub group by sub.career order by career, start_year;"
        students = (sqldf(query)).values.tolist()
        res = {}
        for i in students:
            d = {i[0]:{
                "Year": i[1],
                "Num_of_student": i[2]
            }}
            res.update(d)
        return JsonResponse(res, safe=False ,json_dumps_params={'ensure_ascii': False})
    return JsonResponse("Mismatch Request")            

#####UC03############

@csrf_exempt
def csv2560Download(request, curri, year):
    subjects = list(Subject_Data.objects.all().values())
    if curri == 'computer':
        response = HttpResponse(content_type='text/csv')
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(['student_id','subject_id','grade', 'curriculum', 'Want_To_Predict'])
        for i in subjects:
            print(i['subject_id'])
            writer.writerow(['Optional',i['subject_id'],'Your Grade', 'วิศวกรรมคอมพิวเตอร์'])
        response['Content-Disposition'] = 'attachment; filename="2560fileformat.csv"'
    else:
        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        writer.writerow(['student_id','subject_id','grade', 'curriculum', 'Want_to_Predict'])
        for i in subjects:
            writer.writerow(['Optional',i['subject_id'],'Your Grade', 'วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)'])
        response['Content-Disposition'] = 'attachment; filename="2560fileformat.csv"'
    return response

    #####UC05######
@csrf_exempt
def gradeUploader(request):
    grade_list = ['A','B','C','D','F','S','a','b','c','d','f','s','B+','C+','D+','a','b+','c+','d+']
    csv_file = request.FILES['path_to_csv']
    df = pd.read_csv(csv_file, dtype={0:'string',1:'string', 3:'string', 4:'string', 5:'string'}, encoding='utf-8')
    lis = []
    for index, row in df.iterrows():
        strt = '0'
        subId = row['subject_id']
        grade = row['grade']
        if len(subId) == 7:
            strt += row['subject_id']
            subId = strt
        elif len(subId) < 7 or len(subId) > 8:
            return JsonResponse(f'Error subject id not valid at index : {index}',safe=False)
        df.at[index, 'subject_id'] = subId
        if grade == 'Your Grade':
            df.at[index, 'grade'] = 'Zero'
        elif grade not in grade_list:
            return JsonResponse(f'Error grade not valid at index : {index}',safe=False)
    response = recc.reqPredictPerUser_Production(df)
    for i in response:
        print(i)
    return JsonResponse("Hi", safe=False)

@csrf_exempt
def getPossibleYear(request):
    students = list(Student.objects.all().values())
    df = pd.DataFrame(students)
    year = list(df['start_year'].unique())
    return JsonResponse(year , safe=False, json_dumps_params={'ensure_ascii': False})

#####UC03############

######Register######
class RegisterUser(generics.CreateAPIView):
    queryset = Rec_User.objects.all()
    serializer_class = RecUSerializer
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            if Rec_User.objects.filter(username=username).exists():
                res = {
                "message": "Username already exists.",
                "status": status.HTTP_400_BAD_REQUEST
                }
                return JsonResponse(res, safe=False)

            user = Rec_User()
            user.username = username
            user.set_password(password)
            user.save()

            res = {
            "message": "User registered successfully.",
            "status": status.HTTP_200_OK
            }
            return JsonResponse(res, safe=False)
        res = {
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }
        return JsonResponse(res ,safe=False)

####LOGIN#######
class LoginUser(generics.CreateAPIView):
    queryset = Rec_User.objects.all()
    serializer_class = RecUSerializer
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = Rec_User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
                res = {
                    "message":"Invalid username or password.",
                    "status": status.HTTP_401_UNAUTHORIZED
                }
                return JsonResponse(res, safe=False)
        
        token = jwt.encode({
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, 'secret', algorithm='HS256')
            
        res = {
                "message": token.decode('utf-8'),
                "status": status.HTTP_200_OK
        }
        return JsonResponse(res, safe=False)