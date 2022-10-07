from dataclasses import field
from rest_framework import serializers
from .models import Student, Subject_Data

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=('student_id', 'subject_id', 'grade', 'semester', 'year', 'curriculum')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject_Data
        fields=('subject_id', 'subject_name_thai', 'subject_name_eng', 'abstract', 'subject_key', 'year', 'subject_class')