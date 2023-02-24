from dataclasses import field
from rest_framework import serializers
from .models import Student_Data, Student_Grade, Subject_Data, CSV_File, Rec_User
import pickle as cPickle

class StudentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student_Grade
        fields=('student_id', 'subject_id', 'grade', 'semester', 'year')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student_Data
        fields=('student_id', 'curriculum', 'status', 'career', 'start_year', 'curriculum_year')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject_Data
        fields=('subject_id', 'subject_name_thai', 'subject_name_eng', 'abstract', 'subject_key', 'year', 'subject_class')

class RecUSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rec_User
        fields = ('id', 'username', 'password')