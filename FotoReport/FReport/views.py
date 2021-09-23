from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView
from .forms import Add_report
from .my_def import add_clips, def_add_photo
from django.core.files.storage import FileSystemStorage


# Foto лучше заменить на photo

# HOTKEY - переходы вперед-назад Ctrl + Alt + влево/вправо

def admins_add(request):
    #form = ClipsForm(request.POST)
    form = Add_report(request.POST)
    add_clips()
    return render(request, 'FReport/admins.html', {'form': form})


def foto_add(request):
    #form = ClipsForm(request.POST)
    form = Add_report(request.POST)
    def_add_photo()
    return render(request, 'FReport/admins.html', {'form': form})


def admins(request):
   # print("selected file: " + request.POST["name"])
    form = Add_report(request.POST)
    return render(request, 'FReport/admins.html', {'form': form})


def FO(request):
   # form = FO_ADD()
    return render(request,'FReport/montag.html')


def main(request):

    return render(request,'FReport/main.html')


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'FReport/admins.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'FReport/admins.html')

# Create your views here.
