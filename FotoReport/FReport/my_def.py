
import os, cv2, xlrd, datetime


from .models import *


# Hotkey - найти использование метода Ctrl + Alt + F7

# Добавление новых роликов в базу



def add_clips():  # глагол вначале -> add_clips
    path = "//dc1/Советская/_Clips"  # Хардкод, убрать
    list_files = os.listdir(path)  # список файлов -> file а не директория
    list_add = []
    list_error = []
    for name_file in list_files:  # video_file? file_path?
        find_clips = Clips.objects.filter(name=name_file)  # избегай необщепринятых сокращений - el
        if not find_clips:
            screen_resolution = ''  # понятное название переменной
            if name_file.find('.avi'):  # в константы
                vid = cv2.VideoCapture(path + '/' + name_file)  # Для склейки файлов используется что-то типа path.join
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

            print(str(clip[0]),str(screen[0]) )

            #if clip[0].scr_res != screen[0].scr_res:
                #list_error.append(name_video)
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
            new_entry = PhotoRep(Scr_id=screen[0], Clips_id=clip[0])
            new_entry.save()
    return True

#количество роликов
def count_entry(dict_video):
    count = 0
    for key in dict_video:
        list_video = dict_video[key]
        count += len(list_video)
    return count




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
#    dict_error=check_resolution(dict_video) ## понять как сравниваются поля кверисета
    if dict_error != {}:
        print('Найдены ошибки', dict_error) ##нужен вывод в таблицу на страницу
    #else:
    #    push_entry(dict_video)
    #print(count_entry(dict_video))
    #print(datetime.datetime.today().day)
    #print(datetime.datetime.today().isoweekday())
    #today = datetime.date.today()
    #print(today)


    #print(-today.weekday())
    #print(today + datetime.timedelta(days=-today.weekday(), weeks=1))





    # print( list_error2)
   # print(list_error, list_error2)
