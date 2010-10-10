from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings

import string, os
from subprocess import *


class ImportBookForm(forms.Form):
    book  = forms.FileField()
    convert = forms.BooleanField(required=False, help_text='As well as uploading, also convert to mobi format')


@login_required
def import_book(request):
    if request.method == 'POST':
        form = ImportBookForm(request.POST, request.FILES)
        if form.is_valid():
            try:
               c = request.POST['convert']
            except:
               c = False
            handle_uploaded_book(request.FILES['book'], c)
            return HttpResponseRedirect('/upload/completed/')
    else:
        form = ImportBookForm()
    return render_to_response('upload/import_book.html', {'form': form})


def handle_uploaded_book(f, convert):
    safe_file = '/tmp/' + f.name
    destination = open(safe_file, 'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close() 
    if convert:
        ext = ".mobi"
    else:
        ext = ""
    # However caution advice as a script is run as the user of this process.
    calibre_process = Popen([settings.SCRIPTS + "/calibre-convert-upload.sh", safe_file, ext], stdout=PIPE)
    calibre_process.wait()
    os.remove(safe_file)


@login_required
def completed(request):
    return render_to_response('upload/completed.html')

def welcome(request):
    return render_to_response('upload/welcome.html')

