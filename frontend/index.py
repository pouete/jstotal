import hashlib
from django.shortcuts import render

from django.forms import ModelForm
from django import forms
from frontend import models

# Create your views here.
class UploadForm(ModelForm):
    class Meta:
        model = models.PotentialThreat
        fields=["threatfile","filetype"]

class testform(forms.Form):
    titel = forms.CharField()

def index(request):
    if request.method == 'POST':
        form =  UploadForm( request.POST, request.FILES)
        
        if form.is_valid():
            obj = form.save(commit = False)
            uploadedfile = request.FILES["threatfile"] 
            uploadedfile.seek(0)
            filecontent = uploadedfile.read(uploadedfile._size)
            obj.sha256 =hashlib.sha256(filecontent).hexdigest()
            obj.filename = request.FILES["threatfile"].name
            obj.save()
    else:
        form = UploadForm()
    return render(
            request,
            "index.html",{
                "Form" : form ,
                "test" : "test",
                }
                )

