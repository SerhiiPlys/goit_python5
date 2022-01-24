"""Скрипт написан под мои личные предпочтения с учетом требований ДЗ
   Поскольку наиболее точные требования заказчика (который я сам!!!) знаю только я
   постольку под себя его и сделал. Конечно логика его может меняться. Это версия 1.2021
"""

import os  # work with file system
import sys # for command line
import shutil # for func copy
import re # string func

path_test = "C:\\Users\\Ultra\\Desktop\\garbage"
#for p in sys.argv:
#    path = p


TRANS = {}
def make_trans_dict():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l",
                   "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "",
                   "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    global TRANS
    CYR = []
    for i in CYRILLIC_SYMBOLS:
        CYR.append(i)
    for i,j in zip(CYR, TRANSLATION):
        TRANS[ord(i)] = j
        TRANS[ord(i.upper())] = j.upper()

def check_name(name_a):
    name_a_a = name_a.translate(TRANS)
    return re.sub(r'[^a-zA-Z0-9.]', '_', name_a_a)

def empty_dir(path_a):
    """Проверка что директория пуста - тогда возврат True
       если путь ошибочен или папка не пустая возврат False
    """
    if os.path.exists(path_a):
        sz = os.path.getsize(path_a)
        if sz == 0:
            return True
        else:
            return False
    else:
        return False

def del_empty_dir(path_b):
    """Удаление пустой папки и подпапок, фугкция рекурсивная, ппосокльку
       функция os.rmdir() удаляет только папку без вложенных обьектов,
       поэтому нужно рекусрсивно проходить по поути до нижнего уровня и удалять
       Входя сюда мы уже точно знаем что размер обьекта = 0
    """
    ls_1 = os.listdir(path_b)
    if bool(ls_1) == True:    
        for i in ls_1:                         # ls_1 - список подобьектов в первичной папке
            path_b_a = os.path.join(path_b, i) # путь к подобьекту
            del_empty_dir(path_b_a)            # рекурсивный вызов по дочернему пути 
    else:
        os.rmdir(path_b)  # удаляем папку - она одна без вложенных обьектов
        
    
# проверяем существование каталога и создаем все папки
path = input("Введите путь к папке:\nИспользуйте двойной Бэкслеш \\\ как разделитель\n")
if not os.path.isdir(path):
    print("Папка не найдена")
    os_exit(-1)  # код ошибки
else:
    if not os.path.exists(path+'\\images'):
        os.mkdir(path+'\\images')
    if not os.path.exists(path+'\\documents'):
        os.mkdir(path+'\\documents')
    if not os.path.exists(path+'/audio'):
        os.mkdir(path+'/audio')
    if not os.path.exists(path+'/video'):
        os.mkdir(path+'/video')
    if not os.path.exists(path+'/archives'):
        os.mkdir(path+'/archives')
    if not os.path.exists(path+'/others'):
        os.mkdir(path+'/others')

 # делаем словарь для транслитерализации - путь существует
make_trans_dict()

 #получаем все пути к существующим файлам
ls_files = []
print("Список существующих файлов в выбранной папке:")
for root,dirs,files in os.walk(path):
    for f in files:
        full_adr = os.path.join(root, f)
        print(full_adr)
        ls_files.append(full_adr)
print(' ')

  #раскидываем файлы по папкам назначения согласно расширения
for full_adr_s in ls_files:
    try:
        if (("images" in full_adr_s) or ("documents" in full_adr_s) or
            ("video" in full_adr_s) or ("audio" in full_adr_s) or
            ("archives" in full_adr_s) or ("other" in full_adr_s)):
            continue #пропускаем файлы и пути в сущетствующих папках назначения
        elif ((".xlsx" in full_adr_s) or (".txt" in full_adr_s) or
            (".doc" in full_adr_s) or (".docx" in full_adr_s) or
            (".pdf" in full_adr_s) or (".pptx" in full_adr_s)):
            normal_name = check_name(os.path.basename(full_adr_s))
            full_adr_d = os.path.join(path+'\\documents', normal_name)
            shutil.copyfile(full_adr_s, full_adr_d)
            os.remove(full_adr_s)
            print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
        elif ((".jpeg" in full_adr_s) or (".bmp" in full_adr_s) or
            (".jpg" in full_adr_s) or (".png" in full_adr_s)):
            normal_name = check_name(os.path.basename(full_adr_s))
            full_adr_d = os.path.join(path+'\\images', normal_name)
            shutil.copyfile(full_adr_s, full_adr_d)
            os.remove(full_adr_s)
            print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
        elif ((".avi" in full_adr_s) or (".mpeg" in full_adr_s) or
            (".mp4" in full_adr_s) or (".mov" in full_adr_s)):
            normal_name = check_name(os.path.basename(full_adr_s))
            full_adr_d = os.path.join(path+'\\video', normal_name)
            shutil.copyfile(full_adr_s, full_adr_d)
            os.remove(full_adr_s)
            print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
        elif ((".mp3" in full_adr_s) or (".ogg" in full_adr_s) or
            (".wav" in full_adr_s) or (".amr" in full_adr_s)):
            normal_name = check_name(os.path.basename(full_adr_s))
            full_adr_d = os.path.join(path+'\\audio', normal_name)
            shutil.copyfile(full_adr_s, full_adr_d)
            os.remove(full_adr_s)
            print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
        elif ((".zip" in full_adr_s) or (".rar" in full_adr_s) or
            (".tar" in full_adr_s) or (".gz" in full_adr_s)):
            normal_name = check_name(os.path.basename(full_adr_s))
            full_adr_d = os.path.join(path+'\\archives', normal_name)
            shutil.copyfile(full_adr_s, full_adr_d)
            os.remove(full_adr_s)
            print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
        else:
            normal_name = check_name(os.path.basename(full_adr_s))
            full_adr_d = os.path.join(path+'\\others', normal_name)
            shutil.copyfile(full_adr_s, full_adr_d)
            os.remove(full_adr_s)
            print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
    except:
        print("Ошибка в путях либо копировании файлов")
        os._exit(-2)

   #удаляем пустые папки
print("Список удаляемых пустых папок:")
ls_dirs_1 = os.listdir(path)    # список из папок первого уровня
for d in ls_dirs_1:             #
    full_adr = os.path.join(path, d) 
    if empty_dir(full_adr):
    #try:
        if (("images" in full_adr) or ("documents" in full_adr) or
            ("video" in full_adr) or ("audio" in full_adr) or
            ("archives" in full_adr) or ("other" in full_adr)):
            continue #пропускаем папки в сущетствующих папках назначения
        else:
            print(f"Удаление пустой папки\n{full_adr}")
            del_empty_dir(full_adr) #удаляем папку и подпапки - рекурсия
   #except:
   #     print("Ошибка в удалении пустых папок")
print(' ')

   # распаковываем архивы в подпапки
print("Перемещение и распаковка архивов:")
ls_archives = os.listdir(path+'/archives')
for arc in ls_archives:
    if (".zip" in arc) or (".rar" in arc) or (".tar" in arc):
        arc_n = arc[0:len(arc) - 4]
        os.mkdir(os.path.join(path+'/archives', arc_n))
        try:
            shutil.unpack_archive(arc, os.path.join(path+'/archives', arc_n))
            os.remove(os.path.join(path+'/archives', arc))
        except:
            print(f"{arc} архив неопознан или поврежден")
    elif (".gz" in arc):
        arc_n = arc[0:len(arc) - 3]
        os.mkdir(os.path.join(path+'/archives', arc_n))
        try:
            shutil.unpack_archive(arc, os.path.join(path+'/archives', arc_n))
            os.remove(os.path.join(path+'/archives', arc))
        except:
            print(f"{arc} архив неопознан или поврежден")
    
    



