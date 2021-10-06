from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView
from .forms import Add_report
from .my_def import *
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import FileFieldForm
from .forms import UploadFileForm
from django.views.generic.edit import FormView


# Foto лучше заменить на photo

# HOTKEY - переходы вперед-назад Ctrl + Alt + влево/вправо

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def montag2(request, id):
    screen_clips_list = get_to_report(id)
    # if screen != '' :
    #     return render(request, 'FReport/montag.html', {'screen_clips_list': screen_clips_list})
    return render(request, 'FReport/montag_in.html', {'screen_clips_list': screen_clips_list})

def start_report(request, id, clip=''):
    if request.method == 'GET':
        if clip=='':
            ConectControlSsh.conect_ssh(id)
        else:
            ConectControlSsh.conect_ssh(id, clip)
            clip = ''
    screen_clips_list = get_to_report(id)
    clip = ''
    return render(request, 'FReport/montag_in.html', {'screen_clips_list': screen_clips_list})


def montag(request):

    if request.method == 'GET':
        screen_clips_list = get_to_report(0)
        return render(request, 'FReport/montag.html', {'screen_clips_list': screen_clips_list})
    else:

        screen_clips_list = get_to_report(0)
        return render(request, 'FReport/montag.html', {'screen_clips_list': screen_clips_list})






# def openfile2(request):
#     form = Add_report(request.POST)
#     askopenfilename(
#         initialdir='c:',
#         title="Выберете файл с отчетом",
#         filetypes=(
#             ("Excel", "*.xls"),
#             ("All Files", "*.*")
#         )
#     )
#     return render(request, 'FReport/montag.html', {'form': form})

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
    screen_clips_list = CreateScriptScreen.create_script(0)
    return render(request, 'FReport/admins.html', {'screen_clips_list': screen_clips_list})


def admins(request):
    if request.method == 'POST' and len(request.FILES):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #def_add_photo()
        #return render(request, 'FReport/admins.html')
        #screen_clips_list =
        screen_clips_list = def_add_photo2(uploaded_file_url)
        return render(request, 'FReport/admins.html', {
            'uploaded_file_url': uploaded_file_url, 'screen_clips_list': screen_clips_list
        })
    #return render(request, 'FReport/admins.html')
   # print("selected file: " + request.POST["name"])
    #form = Add_report(request.POST)
    return render(request, 'FReport/admins.html')


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
