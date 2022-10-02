from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Student
from .serializers import StudentSerializer
# Create your views here.

def catch():
    lis = ['a','b','c']
    return lis

def getAllStudent(request):
    students = Student.objects.all()
    students_serializer = StudentSerializer(students,many=True)
    return JsonResponse(students_serializer.data, safe=False)
