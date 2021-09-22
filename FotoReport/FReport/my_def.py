import os, cv2, xlrd
from .models import *


# Добавление новых роликов в базу
def clips_add():
    path = "//dc1/Советская/_Clips"
    list_dir = os.listdir(path)
    list_add = []
    list_error = []
    for el_dir in list_dir:
        el_clips = Clips.objects.filter(name=el_dir)
        if not el_clips:
            qs_el_scr_res = ''
            if el_dir.find('.avi'):
                vid = cv2.VideoCapture(path + '/' + el_dir)
                height = round(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                width = round(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                qs_el_scr_res = Scr_res.objects.filter(scr_res_1=width, scr_res_2=height)
            if (len(qs_el_scr_res)>=1):
                list_add.append(el_dir)
                new_entry = Clips(name=el_dir, scr_res_id=qs_el_scr_res[0])
                new_entry.save()
            else:
                list_error.append(el_dir)
    print(list_error, '/n', list_add)
   # return render(request, 'FReport/admins.html', {'form': form})
#приведение к нормальному виду текста
def text_normal(text):
    text = text.rstrip(',')
    text = text.rstrip()
    text = text.lstrip(',')
    text = text.lstrip()
    text = text.replace("\xa0", "")
    text = text.replace(".avi", "")
    text = text.replace(".", ",")
    text = text.replace(" ", ",")
    text = text.replace(",,", ",")
   # text = text.replace(",", ".avi,")
    list = text.split(',')
    list2 = []
    for el in list:
        if len(el)>10:
            list2.append(el+'.avi')
    return list2






def def_foto_add():
    path = 'c:/ФО 23.09.xls'
    exel = xlrd.open_workbook(path, formatting_info=True)
    sheet = exel.sheet_by_index(0)
    dect = {}
    i = 4
    while i < 28:
        src_name = str(sheet.row_values(i)[1])
        list_clips= text_normal(str(sheet.row_values(i)[2]))
        dect.update({sheet.row_values(i)[1]:list_clips})
        i = i+1

    print(dect.get('09_Мельникайте-Республики [n]'))






