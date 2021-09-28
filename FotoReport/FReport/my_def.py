import os, cv2, xlrd, datetime
import shutil
from settings import BASE_DIR

from typing import List

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

def this_thursday():
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


# Вызов классов
def def_add_photo2(files_report):
    text = str(BASE_DIR)
    text = text.replace('\\', "/")
    text = text + files_report
    text = 'C:/111 (2).xls'
    parser = ExcelFileParser(text)
    screen_clips_list = parser.parse()

    repository = PhotoReportRepository()
    repository.add_clips_to_report(screen_clips_list)


def get_to_report():
    data = this_thursday()
    repository = PhotoReportRepository()
    my_copy = repository.get_to_report(data)
    #print(str(my_copy[00].screen_name.ip_add))

def create_script():
    dict_result = {}
    data = this_thursday()
    repository = PhotoReportRepository()
    script_list = repository.get_to_report(data)
    #print(str(my_copy[00].screen_name.ip_add))
    for script in script_list:
        if len(script.clips) >= 1:
            try:
                file_start_up_script = open('//' + str(script.screen_name.ip_add) + '/'
                                            + script.screen_name.dir + '/StartUpScript.txt', 'w')
            except:
                dict_result[script.screen_name] = "Экран не доступен"
            else:
                file_start_up_script.write('telnet -up' + '\n')
                list_result = 'telnet -up' + '\n'
                file_start_up_script.write('__dev -up' + '\n')
                list_result = list_result + '__dev -up' + '\n'
                for clips_item in script.clips:
                    file_start_up_script.write('play ' + str(clips_item) + '; ')
                    list_result = list_result + 'play ' + str(clips_item) + '; '
                dict_result[script.screen_name] = list_result
                file_start_up_script.close()

    return dict_result



# DTO, хранит данные. Используется для передачи данных внутри программы
class ScreenClips:
    def __init__(self, screen_name: str, clip_list: List[str]):
        self.screen_name = screen_name
        self.clips = clip_list


# Парсер. Его дело - извлечь данные из Excel
class ExcelFileParser:
    def __init__(self, path_to_excel_file: str):
        self._path_to_excel_file = path_to_excel_file

    def parse(self) -> List[ScreenClips]:
        exel = xlrd.open_workbook(self._path_to_excel_file, formatting_info=True)
        sheet = exel.sheet_by_index(0)

        screen_clips = []
        for i in range(4, 28):
            screen_name = str(sheet.row_values(i)[1])
            joined_clips_string = str(sheet.row_values(i)[2])
            clips = normalize_text_creating_list(joined_clips_string)
            screen_clips.append(ScreenClips(screen_name, clips))

        return screen_clips


# Репозиторий. Он знает, как общатья с базой.
class PhotoReportRepository:
    def add_clips_to_report(self, screen_clips_list: List[ScreenClips]):
        wrong_screen_names = [item.screen_name for item in screen_clips_list if not self.is_screen_exist(item.screen_name)]
        if wrong_screen_names:
            print('Экраны не найдены в БД', wrong_screen_names)  ## нужен вывод в таблицу на страницу
            # FIXME: raise exception вместо print/return, после этого вынести в отдельный метод validate
            return

        # TODO: аналогично проверить названия видео
        # TODO: аналогично проверить разрешение

        for screen_clips in screen_clips_list:
            self._save_clips_report(screen_clips)

    @staticmethod
    def is_screen_exist(screen_name: str) -> bool:
        screen = Scr.objects.filter(name=screen_name)
        if screen:
            return True
        else:
            return False

    @staticmethod
    def _save_clips_report(screen_clips: ScreenClips):
        for clip in screen_clips.clips:
            screen_entity = Scr.objects.filter(name=screen_clips.screen_name)
            clip_entity = Clips.objects.filter(name=clip)
            date = find_next_thursday()
            # FIXME: проверить на пустоту
            photorep_entry = PhotoRep.objects.filter(Scr_id=screen_entity[0],
                                                     Clips_id=clip_entity[0],
                                                     data_report=date)
            if (len(photorep_entry)) == 0:
                new_entry = PhotoRep(Scr_id=screen_entity[0], Clips_id=clip_entity[0], data_report=date)
                new_entry.save()
        return True

    @staticmethod
    def get_to_report(data) -> List[ScreenClips]:
        screen_list = Scr.objects.filter(check=True)
        screen_clips = []

        for screen in screen_list:
            clip_list = []
            photo_report_queryset = PhotoRep.objects.filter(data_report=data, Scr_id=screen)
            for clips in photo_report_queryset:
                clip_list.append(clips.Clips_id.name)
            screen_clips.append(ScreenClips(screen, clip_list))


        return screen_clips
