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
from recommend import views as recc

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^hello', view.hello),
    url(r'^throw', view.Throw),
    url(r'^test', view.csvHandler),
    url(r'^downloadCsv',view.csvDownload),
    
    url(r'^students$',recc.studentApi),
    url(r'^students/(?P<id>\w+)$',recc.studentApi),
    url(r'^students/(?P<id>\w+)/(?P<sid>\w+)$',recc.studentApi),
    url(r'^studentsUpdateStatus$',recc.studentUpdateStatus),
    url(r'^studentUpdateCareer$',recc.studentUpdateCareer),
    url(r'^studentUpdateCareer/(?P<id>\w+)$',recc.studentUpdateCareer),
    url(r'^studentThatHaveJob$',recc.getStudentWithJob),
    url(r'^updateStudentStartYear', recc.addStudentStartYear),


    url(r'^myModels$',recc.surpriseModel),

    url(r'^getModel/(?P<curri>\w+)$', recc.generateModel),

    url(r'^uploadSubject$', view.csvHandlerSubject),
    url(r'^subjects$',recc.subjectApi),
    url(r'^subjects/(?P<id>\w+)$',recc.subjectApi),

    #UC03
    url(r'^reqAna/(?P<curri>\w+)/(?P<year>\w+)$', view.csv2560Download),
    url(r'^reqPredict/(?P<model>\w+)$', view.gradeUploader),
    url(r'^getPossibleYear', view.getPossibleYear),

    #UC01
    url(r'^getGradResult/(?P<curri>\w+)/(?P<year>\w+)$', view.uc01_getGradResult),
]
