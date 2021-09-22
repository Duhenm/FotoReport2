import os, cv2, xlrd
from .models import *

# Hotkey - найти использование метода Ctrl + Alt + F7

# Добавление новых роликов в базу
def clips_add():  # глагол вначале -> add_clips
    path = "//dc1/Советская/_Clips"  # Хардкод, убрать
    list_dir = os.listdir(path)  # список файлов -> file а не директория
    list_add = []
    list_error = []
    for el_dir in list_dir:  # video_file? file_path?
        el_clips = Clips.objects.filter(name=el_dir)  # избегай необщепринятых сокращений - el
        if not el_clips:
            qs_el_scr_res = ''  # понятное название переменной
            if el_dir.find('.avi'):  # в константы
                vid = cv2.VideoCapture(path + '/' + el_dir)  # Для склейки файлов используется что-то типа path.join
                height = round(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                width = round(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                qs_el_scr_res = Scr_res.objects.filter(scr_res_1=width, scr_res_2=height)  # Избегай сокращений
            if len(qs_el_scr_res) >= 1:  # Используй автоформатирование кода Shif + Alt + L
                list_add.append(el_dir)
                new_entry = Clips(name=el_dir, scr_res_id=qs_el_scr_res[0])
                new_entry.save()
            else:
                list_error.append(el_dir)
    print(list_error, '/n', list_add)


# return render(request, 'FReport/admins.html', {'form': form})
# приведение к нормальному виду текста

# подумать над название метода и его описание normalize_text
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
        if len(el) > 10:            # MINIMAL_FILE_NAME_LENGTH
            list2.append(el + '.avi')
    return list2


def def_foto_add():
    path = 'c:/ФО 23.09.xls'
    exel = xlrd.open_workbook(path, formatting_info=True)
    sheet = exel.sheet_by_index(0)
    dect = {}
    i = 4               # Магия!!!
    while i < 28:       # Магия!!!
        src_name = str(sheet.row_values(i)[1])
        list_clips = text_normal(str(sheet.row_values(i)[2]))
        dect.update({sheet.row_values(i)[1]: list_clips})
        i = i + 1       # Может использовать for

    print(dect.get('09_Мельникайте-Республики [n]'))
