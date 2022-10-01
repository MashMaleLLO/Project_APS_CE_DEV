from urllib import response
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from recommend import views as recc
import pandas as pd
import csv
from django.views.decorators.csrf import csrf_exempt

def hello(requset):
    return JsonResponse("Hi", safe=False)

def Throw(request):
    a = recc.catch()
    return JsonResponse(a,safe=False)

@csrf_exempt
def csvHandler(request):
    csv_file = request.FILES['path_to_csv']
    df = pd.read_csv(csv_file, encoding='utf-8')
    df = df.head()
    df = df.reset_index()  # make sure indexes pair with number of rows
    lis = []
    for index, row in df.iterrows():
        dic = {
            "StudentID":row['student_id'],
            "SubjectID":row['subject_id'],
            "Grade":row['grade'],
            "Semester":row['semester'],
            "Year":row['year'],
            "Curriculum":row['curriculum']
        }
        lis.append(dic)
    return JsonResponse(lis, safe=False)

def csvDownload(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Fname','Lname','Nname'])
    response['Content-Disposition'] = 'attachment; filename="APS_CE.csv"'
    return response


