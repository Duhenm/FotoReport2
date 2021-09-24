
import os, cv2, xlrd, datetime
import shutil

from .models import *

CLIPS_DIR = "//dc1/Советская/_Clips"
# Hotkey - найти использование метода Ctrl + Alt + F7

# Добавление новых роликов в базу



def add_clips():  # глагол вначале -> add_clips
    list_files = os.listdir(CLIPS_DIR)  # список файлов -> file а не директория
    list_add = []
    list_error = []
    for name_file in list_files:  # video_file? file_path?
        find_clips = Clips.objects.filter(name=name_file)  # избегай необщепринятых сокращений - el
        if not find_clips:
            screen_resolution = ''  # понятное название переменной
            if name_file.find('.avi'):  # в константы
                vid = cv2.VideoCapture(CLIPS_DIR + '/' + name_file)  # Для склейки файлов используется что-то типа path.join
                height = round(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                width = round(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                screen_resolution = Scr_res.objects.filter(scr_res_1=width, scr_res_2=height)  # Избегай сокращений
            if (len(screen_resolution)) >= 1:  # Используй автоформатирование кода Shif + Alt + L
                list_add.append(name_file)
                new_entry = Clips(name=name_file, scr_res_id=screen_resolution[0])
                new_entry.save()
            else:
                list_error.append(name_file)
    print(list_error, '/n', list_add)


# return render(request, 'FReport/admins.html', {'form': form})
# приведение к нормальному виду текста

# подумать над название метода и его описание normalize_text
def normalize_text_creating_list(text):
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
    creating_list = text.split(',')
    normalize_list = []
    for name_video in creating_list:
        if len(name_video) > 10:  # MINIMAL_FILE_NAME_LENGTH
            normalize_list.append(name_video + '.avi')
    return normalize_list


def find_next_thursday():
    if datetime.date.today().weekday() >= 3:
        return datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday() + 10)
    else:
        return datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday() + 3)




#возврат неправельно названых выдео
def check_name(dict_video):
    dict_error = {}
    for key in dict_video:
        list_video = dict_video[key]
        list_error = []
        for name_video in list_video:
            clip = Clips.objects.filter(name=name_video)
            if not clip:
                list_error.append(name_video)
        if len(list_error) != 0:
            dict_error[key] = list_error
    return dict_error

#проверка разрешения экрана и ролика
def check_resolution(dict_video):
    dict_error = {}
    for key in dict_video:
        screen = Scr.objects.filter(name=key)
        list_video = dict_video[key]
        list_error = []
        for name_video in list_video:
            clip = Clips.objects.filter(name=name_video)
            if clip[0].scr_res_id != screen[0].scr_res:
                list_error.append(name_video)
        if len(list_error) != 0:
            dict_error[key] = list_error
    return dict_error

#запись в базу
def push_entry(dict_video):
    for key in dict_video:
        list_video = dict_video[key]
        for name_video in list_video:
            screen = Scr.objects.filter(name=key)
            clip = Clips.objects.filter(name=name_video)
            data = find_next_thursday()
            photorep_entry=PhotoRep.objects.filter(Scr_id=screen[0], Clips_id=clip[0], data_report=data)
            if (len(photorep_entry)) == 0:
                new_entry = PhotoRep(Scr_id=screen[0], Clips_id=clip[0], data_report=data)
                new_entry.save()
    return True

#количество роликов
def count_entry(dict_video):
    count = 0
    for key in dict_video:
        list_video = dict_video[key]
        count += len(list_video)
    return count


#проверка наличия элемента в списке
def item_in_list(list,x):
    for i in list:
        if i == x:
            return True



#копирования файлов на экраны
def copy_files(data_report):
    dict_result = {}
    try:
        os.listdir(CLIPS_DIR)
    except:
        dict_result[CLIPS_DIR] = "Директория с роликами недоступна "
    else:
        scr_queryset = Scr.objects.filter(check=True)
        for scr_item in scr_queryset:
            try:
                list_files_screen = os.listdir('//'+scr_item.ip_add + '/'+ scr_item.dir+'/data')
            except:
                dict_result[scr_item.name] = "Экран не доступен"
            else:
                list_result = []
                photo_report_queryset = PhotoRep.objects.filter(data_report=data_report, Scr_id=scr_item)
                for photo_report_item in photo_report_queryset:
                    try:
                        os.path.exists(CLIPS_DIR+'/' + str(photo_report_item.Clips_id))
                    except:
                        list_result.append(str(photo_report_item.Clips_id) + '  Видеоролик не доступен')
                    else:
                        if not item_in_list(list_files_screen, str(photo_report_item.Clips_id)):
                            try:
                                shutil.copy(CLIPS_DIR+'/' + str(photo_report_item.Clips_id), "//"
                                    + scr_item.ip_add + '/'+ scr_item.dir + '/data/'+ str(photo_report_item.Clips_id))
                            except:
                                list_result.append(str(photo_report_item.Clips_id) + 'Видеоролик не удалось скопировать')
                            else:
                                list_result.append(str(photo_report_item.Clips_id) + '  Видеоролик скорирован')
                    if len(list_result) >= 1:
                        dict_result[scr_item.name] = list_result
    return dict_result





def def_add_photo():
    path = 'c:/ЗАЯВКА.xls'
    exel = xlrd.open_workbook(path, formatting_info=True)
    sheet = exel.sheet_by_index(0)
    dict_video = {}
    i = 4  # Магия!!!
    while i < 28:  # Магия!!!
        src_name = str(sheet.row_values(i)[1])
        list_clips = normalize_text_creating_list(str(sheet.row_values(i)[2]))
        dict_video.update({sheet.row_values(i)[1]: list_clips})
        i = i + 1  # Может использовать for
    dict_error = check_name(dict_video)

    if dict_error != {}:
        print('Найдены ошибки', dict_error) ##нужен вывод в таблицу на страницу
    else:
        dict_error = check_resolution(dict_video)
        if dict_error != {}:
            print('Найдены ошибки', dict_error)  ##нужен вывод в таблицу на страницу
        else:
            push_entry(dict_video)
