from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView
from .forms import Add_report
from .my_def import clips_add, def_foto_add
import os, cv2



def admins_add(request):
    #form = ClipsForm(request.POST)
    form = Add_report(request.POST)
    clips_add()
    return render(request, 'FReport/admins.html', {'form': form})


def foto_add(request):
    #form = ClipsForm(request.POST)
    form = Add_report(request.POST)
    def_foto_add()
    return render(request, 'FReport/admins.html', {'form': form})

def admins(request):
    form = Add_report(request.POST)
    return render(request, 'FReport/admins.html', {'form': form})





def FO(request):
   # form = FO_ADD()
    return render(request,'FReport/montag.html')


def main(request):

    return render(request,'FReport/main.html')

# Create your views here.
