import hashlib
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django import forms
from frontend import models
from frontend.index import UploadForm

def getfile(request,filehash):
    try:
        filemeta =  models.PotentialThreat.objects.get(sha256=filehash)
        filepointer = open(filemeta.threatfile.path)
        filecontent = filepointer.read()
        filepointer.close()
        return filecontent
    except ObjectDoesNotExist:
        return None

def index(request,filehash):
    if not filehash:
        return render(
                request,
                "index.html",{
                    "Form" : UploadForm(),
                    "Error" : "No filehash provided",
                    "latest" : models.PotentialThreat.objects.all().order_by("-submittime")
                    })
    file_content = getfile(request,filehash)
    if not file_content:
        return render(
            request,
            "index.html",{
                "Form" : UploadForm(),
                "Error" : "File hash does not exists",
                "latest" : models.PotentialThreat.objects.all().order_by("-submittime")
                 })
        
    file_content = getfile(request,filehash)
    response = HttpResponse(file_content, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="'+filehash+'"'
    return response
