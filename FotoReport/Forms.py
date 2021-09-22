
import xlrd,  xlwt, os , sys, shutil, threading , paramiko, time

from tkinter.filedialog import *
from threading import Thread
from tkinter.messagebox import *
from tkinter import *

from tkinter import messagebox

top = Tk()
top.geometry("500x500")
def openfile1():
    op1 = askopenfilename(
        initialdir=dirall,
        title="Выберете файл с настройками экрана",
        filetypes=(
            ("Excel", "*.xls"),
            ("All Files", "*.*")
        )
    )
    lab1['text'] = op1


def openfile2():
    op2 = askopenfilename(
        initialdir=dirall,
        title="Выберете файл с отчетом",
        filetypes=(
            ("Excel", "*.xls"),
            ("All Files", "*.*")
        )
    )
    lab2['text'] = op2
    lab3['text'] = "Файл не проверен"

def CheckFile():
    if lab2['text'] == '' : messagebox.showerror("Ошибка", " Неодходимо вначале выбрать файл с отчетом")
    else:
        f2 = lab2['text']
        rb = xlrd.open_workbook(lab2['text'], formatting_info=True)
        sheet = rb.sheet_by_index(0)
        errorcount = 0
        fer = open(f2[0:f2.rfind('/') + 1] + 'error.txt', 'w')
        ListDir = os.listdir(path="//dc1/Советская/_Clips")
        for i in (range(sheet.nrows)):
            if (i > 3) and (str(sheet.row_values(i)[1]) != ''):
                text = str(sheet.row_values(i)[2])
                text = text.rstrip(',')
                text = text.rstrip()
                text = text.lstrip(',')
                text = text.lstrip()
                list1 = text.split(',')
                for st in list1:
                    if len(text) > 5:
                        st = st.rstrip(',')
                        st = st.rstrip()
                        st = st.lstrip(',')
                        st = st.lstrip()
                        if (st.rfind('.avi') == -1) and (st != '') and (len(st) > 5):
                            st2 = st.lstrip() + '.avi'

                        for el in ListDir:
                            flag = '0'
                            if (st2 == el):
                                flag = '1'

                                break
                        if flag != '1':
                            errorcount = errorcount + 1
                            fer.write("\nЭкран " + (str(sheet.row_values(i)[1])) + '\n' + " Не найден файл  " + st2)
                            messagebox.showerror("Ошибка", "\n Экран " + (
                                str(sheet.row_values(i)[1])) + '\n\n' + " Не найден файл  " + st2)
        fer.close()

        if (errorcount == 0):
            lab3['text'] = "Ошибок нет"
            lab3['fg'] = "green"
        else:
            lab3['text'] = "Исправте файл отчета"
            messagebox.showerror("Ошибка",
                                 'Кол-во не соотвествий=' + str(errorcount) + '\n\n' + " описание  в файле error.txt ")


def NewScript():
    if lab3['text'] != 'Ошибок нет': messagebox.showerror("Ошибка", " Неодходимо вначале исправить файл с отчетом")
    else:
        f2 = lab2['text']
        rb = xlrd.open_workbook(lab2['text'], formatting_info=True)
        sheet = rb.sheet_by_index(0)
        rbs = xlrd.open_workbook(dirall+'screen.xls', formatting_info=True)
        sheets = rbs.sheet_by_index(0)
        fer = open(f2[0:f2.rfind('/') + 1] + 'script.txt', 'w')

        for i in (range(sheet.nrows)):
            if (i > 3) and (str(sheet.row_values(i)[1]) != ''):
                text = str(sheet.row_values(i)[2])
                s1 = str(sheet.row_values(i)[1])
                s1 = s1[0]+s1[1]
                data1 = "/ATV/data/"
                if s1 == '11' :
                    print(s1)
                    if ((str(sheet.row_values(i)[3]).find('Ст.А'))== -1):
                        s1=10
                    else:
                        data1 = "/ATV2/data/"


                dr = '111'
                for i2 in (range(sheets.nrows)):
                    s2 = str(sheets.row_values(i2)[0])
                    if s2 == s1 :
                        host = str(sheets.row_values(i2)[1])
                        list1 = host.split('\\')
                        host = list1[2]
                        dr = "//" + host + '/ATV/StartUpScript.txt'
                        if s1 == 11:
                            dr = "//" + host + '/ATV2/StartUpScript.txt'
                if dr != '111':
                    print(dr)
                    sc = open(dr, 'w')
                    sc.write('telnet -up' + '\n')
                    sc.write('__dev -up' + '\n')
                text = text.rstrip(',')
                text = text.rstrip()
                text = text.lstrip(',')
                text = text.lstrip()
                list1 = text.split(',')
                fer.write("Экран " + (str(sheet.row_values(i)[1])) + '\n')
                for st in list1:
                    if len(text) > 5:
                        st = st.rstrip(',')
                        st = st.rstrip()
                        st = st.lstrip(',')
                        st = st.lstrip()
                        if (st.rfind('.avi') == -1) and (st != ''):
                            st2 = st.lstrip() + '.avi'
                            fer.write("play " + st2 + '; ')
                            if dr != '111':
                                #print("Экран " + (str(sheet.row_values(i)[1])) + '\n')
                                sc.write("play " + st2 + '; ')
                                file1 = "//" +host+data1+ st2
                                try:
                                    os.path.exists(file1)
                                except IOError as e: print("Экран "+(str(sheet.row_values(i)[1]))+" не доступен ")
                                else:
                                    if not os.path.exists(file1):
                                        shutil.copy("//dc1/Советская/_Clips/" + st2,"//" + host + data1 + st2)
                                        print("Копируется--> " + host + data1 + st2)
#                                    try:
#                                        shutil.copy("//dc1/Советская/_Clips/" + st2,
#                                                    "//" + host + data1 + st2)
#                                    except IOError as e: print('Не удалось скопировать--> '
#                                                               +host+data1+ st2)
#                                    else:
#                                        print("Копируется--> " + host + data1 + st2)


                fer.write('\n\n\n')
                if dr != '111': sc.write(' exec c:\start_t.cmd')
                sc.close()

        lab4['text'] = "Скрипт сформирован"
        lab4['fg'] = "green"
        fer.close()

def connect1():
#    print(thefile)
    rbser = xlrd.open_workbook(lab1['text'], formatting_info=True)
    sheetser = rbser.sheet_by_index(0)
    for iser in (range(sheetser.nrows)):
        cmd = 'net use ' + str(sheetser.row_values(iser)[1]) + ' /user:screen D)minant1'
        print(cmd)
        os.system(cmd)
#    th.join(120)








def NewCopy():
    answer  = e1.get()
    if len(answer) == 1:
        answer = '0' + answer
    rb = xlrd.open_workbook(dirall+'screen.xls', formatting_info=True)
    sheet = rb.sheet_by_index(0)
    for i in (range(sheet.nrows)):
        # print(answer,str(sheet.row_values(i)[0]))
        if answer == str(sheet.row_values(i)[0]):
            host = str(sheet.row_values(i)[1])
            list1 = host.split('\\')
            host = list1[2]
            print(host)
    user = 'Screen'
    secret = 'D)minant1'
    port = 22
    pdir = 'D:/ATVStream'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Подключение
    client.connect(hostname=host, username=user, password=secret, port=port)

    # Выполнение команды
    stdin, stdout, stderr = client.exec_command('schtasks /end /tn CS')
    time.sleep(3)
    stdin, stdout, stderr = client.exec_command('taskkill /IM ATV* /f')
    stdin, stdout, stderr = client.exec_command('taskkill /IM javaw.exe /f')
    stdin, stdout, stderr = client.exec_command('taskkill /IM cityscreen-player.exe /f')
    if answer == '11' :
        stdin, stdout, stderr = client.exec_command('schtasks /run /tn ATV2')
    else:
        stdin, stdout, stderr = client.exec_command('schtasks /run /tn ATV')

    # Читаем результат
    #data = stdout.read() + stderr.read()
    client.close()


dirall = '//dc1/Советская/_Отдел продаж ДМ/_ФО/'
B1 = Button(top, text = "Файл с экранами", width=15,height=1, command = openfile1)
B1.place(x = 15,y = 20)
lab1 = Label(width=30, height=1, bg='grey', fg='white',font=("arial", 12, "bold"))
lab1['text'] = dirall+"screen.xls"
lab1.place(x = 135,y = 20)
B2 = Button(top, text = "Фото отчет", width=15,height=1, command = openfile2)
B2.place(x = 15,y = 55)
lab2 = Label(width=30, height=1, bg='grey', fg='white',font=("arial", 12, "bold"))
lab2['text'] = ""
lab2.place(x = 135,y = 55)
B3 = Button(top, text = "Выполнить проверку",  width=25,height=1, command = CheckFile)
B3.place(x = 15,y = 90)
lab3 = Label(width=18, height=1,  fg='red',font=("arial", 14, "bold"))
lab3.place(x = 215,y = 90)
B4 = Button(top, text = "Сформировать скрит", width=25,height=1, command = NewScript)
B4.place(x = 15,y = 125)
lab4 = Label(width=20, height=1, fg='red',font=("arial", 12, "bold"))
lab4['text'] = 'Скрипт не сформирован'
lab4.place(x = 215,y = 125)
e1 = Entry(width=5)
e1.place(x = 215,y = 160)

B5 = Button(top, text = "Включить фотоотчет", width=25,height=1, command = NewCopy)
B5.place(x = 15,y = 160)




#th = Thread(target=connect1, args =thefile1)
#th.start()





top.mainloop()

