from django import forms
from .models import *


#class FO_ADD(forms.Form):
#    created_at = forms.DateTimeField(auto_now_add=True, verbose_name='Дата')
#    Scr_id = forms.ModelChoiceField(queryset=Scr.name)
#    Clips_id = forms.ModelChoiceField(queryset=Clips.name)


class ClipsForm(forms.ModelForm):
    class Meta:
        model = Clips
        fields = ['name', 'scr_res_id']


class Scr_res_Form(forms.ModelForm):
    class Meta:
        model = Scr_res
        fields = ['scr_res_1', 'scr_res_2', 'id']

class Add_report(forms.Form):
     name = forms.FileField(label='Выберете файл с фотоотчетом', required=False)
 #    name2 = forms.CharField(max_length=100, label='Название ролика')
#    created_at = forms.DateTimeField(label='Дата добавления ролика')
#    updated_at = forms.DateTimeField(label='Дата изменения записи')
#    photo = forms.ImageField(label='Превью', required=False)
 #   scr_res_1 = forms.IntegerField(label='Разрешение видео', initial=384)
 #   scr_res_2 = forms.IntegerField(label='Разрешение видео', initial=288)