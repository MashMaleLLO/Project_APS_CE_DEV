import re
from urllib import response
from django.http.response import JsonResponse
from django.http import HttpResponse
from recommend import views as recc
from recommend.models import Student, Subject_Data, CSV_File
from recommend.serializers import StudentSerializer, SubjectSerializer, CSVSerializer
import pandas as pd
import csv
import codecs
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
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

def hello(requset):
    return JsonResponse("Hi", safe=False)

def Throw(request):
    a = recc.catch()
    return JsonResponse(a,safe=False)

@csrf_exempt
def csvHandler(request):
    csv_file = request.FILES['path_to_csv']
    df = pd.read_csv(csv_file, dtype={0:'string',1:'string', 2:'string', 3:'string', 4:'string', 5:'string' , 6:'string'}, encoding='utf-8')
    print(df)
    lis = []
    for index, row in df.iterrows():
        strt = '0'
        subId = row['subject_id']
        if len(subId) < 8:
            strt += row['subject_id']
            subId = strt
        df.at[index, 'subject_id'] = subId
    res = recc.addStudent(df)
    return JsonResponse(res, safe=False)
    


@csrf_exempt
def csv_upload(request, type_data):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse("File format not match pls upload only .csv file", safe=False)
        df = pd.read_csv(csv_file)
        df = df.astype(str) # cast all columns to str
        pickled_data = cPickle.dumps(df)
        csv_m = {
            "name": csv_file.name,
            "upload_date": datetime.now(pytz.timezone('Asia/Bangkok')),
            "update_date": datetime.now(pytz.timezone('Asia/Bangkok')),
            "del_flag": "0",
            "type_data": type_data,
            "file": pickled_data
        }
        csv_m = CSVSerializer(csv_m, data=csv_m)
        if csv_m.is_valid():
            csv_m.save()
            return JsonResponse(f'Upload file {csv_file.name} complete.', safe=False)
        else:
            return JsonResponse('serializer is not valid',safe=False)
    return JsonResponse('Method not match.', safe=False)


@csrf_exempt
def csvHandlerSubject(request):
    nltk.download('stopwords')
    STOPWORDS = set(stopwords.words('english'))
    nlp = en_core_web_sm.load()
    csv_file = request.FILES['path_to_csv']
    df_subject_pre_nlp = pd.read_csv(csv_file,dtype={0:'string',1:'string', 2:'string', 3:'string', 4:'string', 5:'string', 6:'string', 7:'string'},encoding='utf-8')
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
    return JsonResponse(res, safe=False)


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