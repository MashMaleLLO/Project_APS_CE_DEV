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
    df = pd.read_csv(csv_file, dtype={0:'string',1:'string', 2:'string', 3:'string', 4:'string', 5:'string'}, encoding='utf-8')
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

def csvDownload(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Fname','Lname','Nname'])
    response['Content-Disposition'] = 'attachment; filename="APS_CE.csv"'
    return response


