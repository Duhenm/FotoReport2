from tkinter.filedialog import askopenfilename
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView
from .forms import Add_report
from .my_def import *
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from tkinter import *
from .forms import FileFieldForm
from .forms import UploadFileForm
from django.views.generic.edit import FormView


# Foto лучше заменить на photo

# HOTKEY - переходы вперед-назад Ctrl + Alt + влево/вправо

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)




def montag(request):
    data = this_thursday()
    repository = PhotoReportRepository()
    script_list = repository.get_to_report(data)
#    res = ''
#    for script in script_list:
#        if len(script.clips) >= 1:
#            res += f'<div>\n<p>{script.screen_name}</p>\n<hr>'

    return render(request, 'FReport/montag.html', {'form': form})



class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)





def openfile2(request):
    form = Add_report(request.POST)
    askopenfilename(
        initialdir='c:',
        title="Выберете файл с отчетом",
        filetypes=(
            ("Excel", "*.xls"),
            ("All Files", "*.*")
        )
    )
    return render(request, 'FReport/montag.html', {'form': form})

def admins_add(request):
    #form = ClipsForm(request.POST)
    form = Add_report(request.POST)
    add_clips()
    return render(request, 'FReport/admins.html', {'form': form})


def foto_add(request):
    #form = ClipsForm(request.POST)
    form = Add_report(request.POST)
    def_add_photo2()
    return render(request, 'FReport/admins.html', {'form': form})


def create_sc(request):
    #form = ClipsForm(request.POST)
    form = Add_report(request.POST)
    create_script()
    return render(request, 'FReport/admins.html', {'form': form})


def admins(request):
    if request.method == 'POST' and len(request.FILES):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        def_add_photo2(uploaded_file_url)
        return render(request, 'FReport/admins.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'FReport/admins.html')
   # print("selected file: " + request.POST["name"])
    #form = Add_report(request.POST)
    #return render(request, 'FReport/admins.html', {'form': form})


def FO(request):
   # form = FO_ADD()
    return render(request,'FReport/montag.html')


def main(request):

    return render(request,'FReport/main.html')


def simple_upload(request):
    if request.method == 'POST' and len(request.FILES):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'FReport/simple_upload.html', {
            'FReport/uploaded_file_url': uploaded_file_url
        })
    return render(request, 'FReport/simple_upload.html')






def click_copy_files(request):
    #form = ClipsForm(request.POST)
    form = Add_report(request.POST)
    copy_files(find_next_thursday())
    return render(request, 'FReport/admins.html', {'form': form})

# Create your views here.
