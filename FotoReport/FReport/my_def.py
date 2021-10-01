import os, cv2, xlrd, datetime
import shutil
import time

import paramiko as paramiko

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
    text = text.replace("\n", "")
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

class ConectControlSsh():
    def __init__(self, screen_nam: int, clip: str):
        self._screen_nam = screen_nam
        self._clip = clip

    @staticmethod
    def conect_ssh(id: int, clip=''):
        screen = PhotoReportRepository.get_screen(id)
        user = 'Screen'
        secret = 'D)minant1'
        port = 22
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        host = screen.ip_add
        client.connect(hostname=host, username=user, password=secret, port=port)
        if clip == '':
            CreateScriptScreen.create_script(id)
            client.exec_command('schtasks /end /tn CS')
            time.sleep(2)
            client.exec_command('taskkill /IM ATV* /f')
            client.exec_command('taskkill /IM javaw.exe /f')
            client.exec_command('taskkill /IM cityscreen-player.exe /f')
            client.exec_command('schtasks /run /tn ATV')
        else:
            CreateScriptScreen.create_script(id, clip)
            client.exec_command('schtasks /end /tn ATV')
            time.sleep(2)
            client.exec_command('taskkill /IM ATV* /f')
            client.exec_command('schtasks /run /tn ATV')
            time.sleep(6)
            client.exec_command('schtasks /end /tn ATV')
            client.exec_command('taskkill /IM ATV* /f')

        client.close()





def find_next_thursday():
    if datetime.date.today().weekday() >= 3:
        return datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday() + 10)
    else:
        return datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday() + 3)

def this_thursday():
    return datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday() + 3)







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



class CreateScriptScreen:
    def __init__(self, screen_number: int, clip=''):
        self._screen_number = screen_number
        self._clip = clip

    @staticmethod
    def create_script(screen_number: int, clip='') -> List:
        list_result = []
        data = this_thursday()
        repository = PhotoReportRepository()
        script_list = repository.get_to_report(data, screen_number)
        for script in script_list:
            if len(script.clips) >= 1:
                try:
                    file_start_up_script = open('//' + str(script.screen.ip_add) + '/'
                                                + script.screen.dir + '/StartUpScript.txt', 'w')
                except:
                    list_result.append(str(script.screen) + "   Экран не доступен")
                else:
                    file_start_up_script.write('telnet -up' + '\n')
                    file_start_up_script.write('__dev -up' + '\n')
                    if clip == '':
                        for clips_item in script.clips:
                            file_start_up_script.write('play ' + str(clips_item) + '; ')
                        file_start_up_script.write(' exec c:\start_t.cmd')
                    else:
                        file_start_up_script.write('play ' + clip + '; ')
                        file_start_up_script.write(' exit')
                    file_start_up_script.close()
                    list_result.append(str(script.screen) + "   Скипт сформирован")
        return list_result




# DTO, хранит данные. Используется для передачи данных внутри программы
class ScreenClips:
    def __init__(self, screen: str, clip_list: List[str]):
        self.screen = screen
        self.clips = clip_list

class ScreenClass:
    def __init__(self, name: str, num: int, dir: str, ip_add: str):
        self.name = name
        self.num = num
        self.dir = dir
        self.ip_add = ip_add


# Парсер. Его дело - извлечь данные из Excel
class ExcelFileParser:
    def __init__(self, path_to_excel_file: str):
        self._path_to_excel_file = path_to_excel_file

    def parse(self) -> List[ScreenClips]:
        exel = xlrd.open_workbook(self._path_to_excel_file, formatting_info=True)
        sheet = exel.sheet_by_index(0)

        screen_clips = []
        for i in range(4, 28):
            screen = str(sheet.row_values(i)[1])
            joined_clips_string = str(sheet.row_values(i)[2])
            clips = normalize_text_creating_list(joined_clips_string)
            screen_clips.append(ScreenClips(screen, clips))

        return screen_clips



# Вызов классов
def def_add_photo2(files_report) -> List[ScreenClips]:
    text = str(BASE_DIR)
    text = text.replace('\\', "/")
    text = text + files_report
    parser = ExcelFileParser(text)
    screen_clips_list = parser.parse()

    repository = PhotoReportRepository()

    if len(repository.add_clips_to_report(screen_clips_list)) != 0:
        screen_clips_list = repository.add_clips_to_report(screen_clips_list)

    return screen_clips_list


def get_to_report(id) -> List[ScreenClips]:
    data = this_thursday()
    repository = PhotoReportRepository()
    return repository.get_to_report(data, id)
    #print(str(my_copy[00].screen_name.ip_add))


# Репозиторий. Он знает, как общатья с базой.
class PhotoReportRepository:
    def add_clips_to_report(self, screen_clips_list: List[ScreenClips]) -> dict:
        wrong_screen_names = [item.screen for item in screen_clips_list if not self.is_screen_exist(item.screen)]
        if wrong_screen_names:
            print('Экраны не найдены в БД', wrong_screen_names)  ## нужен вывод в таблицу на страницу
            # FIXME: raise exception вместо print/return, после этого вынести в отдельный метод validate
        if len(self.validate(screen_clips_list)) == 0:
            for screen_clips in screen_clips_list:
                self._save_clips_report(screen_clips)
        else:

            return self.validate(screen_clips_list)
    @staticmethod
    def is_screen_exist(screen_name: str) -> bool:
        screen = Scr.objects.filter(name=screen_name)
        if screen:
            return True
        else:
            return False

    @staticmethod
    def is_clip_exist(clip: str) -> bool:
        clip = Clips.objects.filter(name=clip)
        if clip:
            return True
        else:
            return False


    @staticmethod
    def validate(screen_clips_list: List[ScreenClips]) -> dict:
        def is_clip_exist(clip: str) -> bool:
            clip = Clips.objects.filter(name=clip)
            if clip:
                return True
            else:
                return False
        dict_result = {}
        for screens in screen_clips_list:
            screen = Scr.objects.filter(name=screens.screen)
            list_result = []
            for clips in screens.clips:
                if not is_clip_exist(clips):
                    list_result.append(clips + 'Ролик не найден')
                else:
                    clip = Clips.objects.filter(name=clips)
                    if clip[0].scr_res_id != screen[0].scr_res:
                        list_result.append(clip[0].name + 'Разрешение не соотвествует')
            if len(list_result) != 0:
                dict_result[screens] = list_result
        return dict_result


    @staticmethod
    def _save_clips_report(screen_clips: ScreenClips):
        for clip in screen_clips.clips:
            screen_entity = Scr.objects.filter(name=screen_clips.screen)
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
    def get_to_report(data, id: int) -> List[ScreenClips]:
        if id == 0:
            screen_list = Scr.objects.filter(check=True)
        else:
            screen_list = Scr.objects.filter(check=True, id=id)
        screen_clips = []
        for screen in screen_list:
            clip_list = []
            photo_report_queryset = PhotoRep.objects.filter(data_report=data, Scr_id=screen)
            for clips in photo_report_queryset:
                clip_list.append(clips.Clips_id.name)
            screen_clips.append(ScreenClips(screen, clip_list))
        return screen_clips
    @staticmethod
    def get_screen(id: int) -> ScreenClass:
        screen_query = Scr.objects.filter(check=True, id=id)
       # print(screen_query[0].nameb, screen_query[0].dir)
        screen = ScreenClass(screen_query[0].name, screen_query[0].nameb, screen_query[0].dir, str(screen_query[0].ip_add))
        return screen