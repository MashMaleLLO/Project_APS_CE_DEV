import re
from urllib import response
from django.http.response import JsonResponse
from django.http import HttpResponse
from recommend import views as recc
from recommend.models import Student_Data, Student_Grade,Subject_Data, CSV_File, Rec_User
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
from datetime import datetime, timedelta
# nltk.download('stopwords')
from nltk.corpus import stopwords
# STOPWORDS = set(stopwords.words('english'))
# nlp = en_core_web_sm.load()

from rest_framework import generics, status, authentication, permissions
import jwt

def hello(requset):
    student_data = pd.DataFrame(list(Student_Data.objects.all().values()))
    student_grade = pd.DataFrame(list(Student_Grade.objects.all().values()))
    result = pd.merge(student_grade, student_data, how='left', on='student_id')
    result = result[['student_id', 'subject_id', 'grade', 'semester', 'year', 'curriculum']]
    print(result)
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
def csv_upload(request, id=0, type_data='ข้อมูลรายวิชา'):
    if request.method == 'POST':
        csv_file = None
        if 'path_to_csv' in request.FILES:
            csv_file = request.FILES['path_to_csv']
            if not csv_file.name.endswith('.csv'):
                res = {"message":"File format not match pls upload only .csv file", "status" : status.HTTP_400_BAD_REQUEST}
                return JsonResponse(res, safe=False)
            df = pd.read_csv(csv_file, encoding='utf-8')
            print(df)
            df = df.astype(str) # cast all columns to str
            pickled_data = cPickle.dumps(df)
            if pickled_data:
                csv_m = CSV_File(name = csv_file.name, upload_date = datetime.now(pytz.timezone('Asia/Bangkok')), update_date = datetime.now(pytz.timezone('Asia/Bangkok')), del_flag = "0", type_data = type_data, file = pickled_data)
                csv_m.save()
                res = {"message": f'Upload file {csv_file.name} complete.', "status" : status.HTTP_200_OK}
            else:
                res = {"message":"serializer is not valid", "status" : status.HTTP_400_BAD_REQUEST}
        else:
            res = {"message":"error can't find any find pls upload again", "status" : status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)
    elif request.method == 'PUT':
        if id == 0:
            res = {"message": "Pls enter file id", "status": status.HTTP_400_BAD_REQUEST}
        else:
            this_file = list(CSV_File.objects.filter(id = id).values())
            if this_file == []:
                res = {"message": f'Can\'t find the file with id {id}' , "status": status.HTTP_400_BAD_REQUEST}
            else:
                this_file = CSV_File.objects.get(id=id)
                csv_file = None
                if 'path_to_csv' in request.FILES:
                    csv_file = request.FILES['path_to_csv']
                    if not csv_file.name.endswith('.csv'):
                        res = {"message": "File format not match pls upload only .csv file", "status": status.HTTP_400_BAD_REQUEST}
                        return JsonResponse(res, safe=False)
                    df = pd.read_csv(csv_file, encoding='utf-8')
                    print(df)
                    df = df.astype(str) # cast all columns to str
                    pickled_data = cPickle.dumps(df)
                    if pickled_data:
                        if request.body:
                            up_date_file_info = json.loads(request.body)
                            new_name = up_date_file_info['name']
                            new_type_data = up_date_file_info['type_data']
                        else:
                            new_name = csv_file.name
                            new_type_data = this_file.type_data
                        old_name = this_file.name
                        this_file.name = new_name
                        this_file.type_data = new_type_data
                        this_file.file = pickled_data
                        this_file.save()
                        res = {"message": f'Update file {old_name} to {new_name} complete.', "status": status.HTTP_200_OK}
                    else:
                        res = {"message": f'serializer is not valid for file {csv_file.name}', "status": status.HTTP_400_BAD_REQUEST}
                else:
                    if request.body:
                        old_name = this_file.name
                        up_date_file_info = json.loads(request.body)
                        new_name = up_date_file_info['name']
                        new_type_data = up_date_file_info['type_data']
                        this_file.name = new_name
                        this_file.type_data = new_type_data
                        this_file.save()
                        res = {"message": f'Update file {old_name} to {new_name} complete.', "status": status.HTTP_200_OK}
                    else:
                        res = {"message": "can't not find information to update", "status": status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)
    else:
        res = {"message": "Method not match.", "status": status.HTTP_400_BAD_REQUEST}
        return JsonResponse(res, safe=False)

@csrf_exempt
def file_recover(request, id=0):
    if id == 0:
        res = {"message":"Pls enter a file id", "status" : status.HTTP_400_BAD_REQUEST}
    else:
        recov_file_check = list(CSV_File.objects.filter(id=id).values())
        if recov_file_check == []:
            res = {"message": f'can\'t find file with id {id}', "status": status.HTTP_400_BAD_REQUEST}
        else:
            recov_file = CSV_File.objects.get(id=id)
            if recov_file.del_flag == '0':
                res = {"message": f'This file with id : {id} name : {recov_file.name} isn\'t delete yet.', "status" : status.HTTP_400_BAD_REQUEST}
            else:
                recov_file.del_flag = '0'
                recov_file.save()
                res = {"message": f'Complete recover file {recov_file.name}.', "status": status.HTTP_400_BAD_REQUEST}
    return JsonResponse(res, safe=False) 


@csrf_exempt
def csv_delete_handler(request):
    today = datetime.now(pytz.timezone('Asia/Bangkok'))
    del_file = []
    flag_file = pd.DataFrame(list(CSV_File.objects.filter(del_flag = 1).values()))
    flag_file = flag_file[['id','name','update_date','del_flag']].to_dict('records')
    for i in flag_file:
        if (today - datetime.strptime(str(i['update_date']), '%Y-%m-%d %H:%M:%S.%f%z').astimezone(pytz.timezone('Asia/Bangkok'))).days >= 7:
            del_file.append({'id':i['id'], 'name': i['name']})
    if del_file == []:
        res = {"message": "No file to delete", "status": status.HTTP_200_OK}
    else:
        for j in del_file:
            this_file = CSV_File.objects.get(id = j['id'])
            f_name = j['name']
            this_file.delete()
            print(f'Delete file {f_name}')
        res = {"message": "delete all flage file that over 7 days", "status": status.HTTP_200_OK}
    return JsonResponse(res, safe=False)



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

# @csrf_exempt
# def uc01_getGradResult(request, curri, year):
#     if curri == "com":
#         curri = "วิศวกรรมคอมพิวเตอร์"
#     else:
#         curri = "วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)"
#     query = Q(curriculum = str(curri))
#     query.add(Q(start_year = str(year)), Q.AND)
#     students = list(Student.objects.filter(query).values())
#     df = pd.DataFrame(students)
#     query = "SELECT student_id, start_year, career, curriculum FROM df group by student_id"
#     df = sqldf(query)
#     students = df.values.tolist()
#     if students != []:
#         return JsonResponse(students , safe=False, json_dumps_params={'ensure_ascii': False})
#     else:
#         return JsonResponse("Can not Found any students" , safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def uc02_getPredResultByYear(request, curri, year):
    return 1


### UC01 ###
@csrf_exempt
def get_career_result(request, curri='Default'):
    if request.method == 'GET':
        students = Student_Data.objects.all()
        students = pd.DataFrame(list(students.values()))
        if curri == 'Default':
            query = "select start_year, career,count(student_id) count_student from students where career <> \'Zero\' and (curriculum = \'วิศวกรรมคอมพิวเตอร์\' or curriculum = \'วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)\') group by start_year, career order by start_year, career"
        else:
            query = f'select start_year, career,count(student_id) count_student from students where career <> \'Zero\' and curriculum = \'{curri}\' group by start_year, career order by start_year, career'
        students = (sqldf(query)).values.tolist()
        res = {}
        for i in students:
            d = {i[1]:{
                "Year": i[2],
                "Num_of_student": i[0]
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
                'exp': datetime.utcnow() + timedelta(days=1)
            }, 'secret', algorithm='HS256')
            
        res = {
                "message": token.decode('utf-8'),
                "status": status.HTTP_200_OK
        }
        return JsonResponse(res, safe=False)