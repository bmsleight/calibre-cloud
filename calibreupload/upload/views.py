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
    # Little security hole. Try to pass settings.SCRIPTS as your own path. Then setting.CALIBRE_USER will run a script.
    # Hence careful with setting.*
    # However once you have control of settings.SCRIPTS you can do much worse things - IMHO.
    # However caution adviced.
    calibre_process = Popen(["sudo",  settings.SCRIPTS + "/run-calibre-convert-upload.sh", settings.CALIBRE_USER, settings.SCRIPTS, safe_file, ext], stdout=PIPE)
    calibre_process.wait()
    os.remove(safe_file)


@login_required
def completed(request):
    return render_to_response('upload/completed.html')

