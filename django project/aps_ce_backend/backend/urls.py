"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path as url
from backend import view
from backend.view import RegisterUser, LoginUser
from recommend import views as recc

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^hello$', view.hello),
    url(r'^fileUpload$', view.csv_upload),  # Api gate way for upload file

    url(r'^getFile', recc.file_api),  # Api gate way for upload file
    # Api gate way for upload file
    url(r'^getFile/(?P<id>\w+)$', recc.file_api),
    # Api gate way for delete flag files
    url(r'^delFlageFile$', view.csv_delete_handler),
    # Api gate way for recover flag files
    url(r'^recoverFile/(?P<id>\w+)$', view.file_recover),
    url(r'^editFileContent/(?P<id>\w+)$', recc.file_content_edit),

    # url(r'^downloadCsv',view.csvDownload),

    # Up CSV to student data and grade
    url(r'^ingest_student_csv', view.student_grade_database_handler),

    url(r'^ingest_subject_csv', view.subject_csv_upload_hander),  # Up CSV to subject

    # Api gate way of student data
    url(r'^students_data$', recc.student_data_api),
    # Api gate way of student data
    url(r'^students_data/(?P<id>\w+)$', recc.student_data_api),
    url(r'^students_data/(?P<id>\w+)/(?P<curri>\w+)$',
        recc.student_data_api),  # Api gate way of student data

    # Api gate way of student grade
    url(r'^students_grade$', recc.student_grade_api),
    # Api gate way of student grade
    url(r'^students_grade/(?P<st_id>\w+)$', recc.student_grade_api),
    url(r'^students_grade/(?P<st_id>\w+)/(?P<su_id>\w+)$',
        recc.student_grade_api),  # Api gate way of student grade

    # Api gate way of update career
    url(r'^update_career$', view.update_career),

    # url(r'^studentUpdateCareer$',recc.studentUpdateCareer),
    # url(r'^studentUpdateCareer/(?P<id>\w+)$',recc.studentUpdateCareer),
    url(r'^studentThatHaveJob$', recc.getStudentWithJob),


    url(r'^myModels$', recc.surpriseModel),  # api สร้าง model rec

    url(r'^create_Rec_Model$', recc.generateRecModel_manyUser),

    url(r'^create_Career_Model$', recc.create_career_model),

    url(r'^uploadSubject$', view.nlp_subject_handler),
    url(r'^subjects$', recc.subjectApi),
    url(r'^subjects/(?P<id>\w+)$', recc.subjectApi),

    url(r'^req_pred_many', recc.reqPredict_career_manyUser),

    # UC03
    url(r'^reqAna', view.csv_template_generator),  # สร้าง file csv
    url(r'^reqPredict', view.gradeUploader),
    url(r'^getPossibleYear', view.getPossibleYear),
    # UC01
    url(r'^getCareerResult/', view.get_career_result),

    # url(r'^getGradResult/(?P<curri>\w+)/(?P<year>\w+)$', view.uc01_getGradResult),

    url(r'^register', RegisterUser.as_view(), name='register'),

    url(r'^signin', LoginUser.as_view(), name='login'),

    # UC06
    url(r'^recommendSubject', view.recommendSubject),
    url(r'^keysubject', view.keySubject),
]
