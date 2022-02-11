import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def main():
    global event
    global keyboard
    global vk
    global upload
    global longpoll
    global dataBase
    global zad
    vk_session = vk_api.VkApi(
        token=open('token.txt', 'r').read())
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk)
    zad = VkKeyboard(one_time=True)
    hl = VkKeyboard(one_time=True)
    photos = {'tM': photo([r'files\TablMendel.jpg']), 'tR': photo([r'files\TablRastv.jpg']),
              'rA': photo([r'files\RyadAktivn.jpg'])}
    files = {'SVKO': r'files\SVKO.txt', 'SVK': r'files\SVK.txt', 'SVNO': r'files\SVNO.txt', 'SVOO': r'files\SVOO.txt',
             'SVS': r'files\SVS.txt', 'SVSch': r'files\SVSch.txt', 'EH': 'files\ExHelp.txt', 'H': 'files\Help.txt'}
    atm = {'mass': ('молярную массу', 'молярная масса'), 'elem': ('знак', 'знак'), 'num': ('порядковый номер', 'порядковый номер')}
    kisl = {'form': ('формулу', 'формула'), 'name': ('имя', 'название'), 'ost': ('остаток', 'остаток')}
    zad.add_button('Дальше', color=VkKeyboardColor.POSITIVE)
    zad.add_button('Стоп', color=VkKeyboardColor.NEGATIVE)
    hl.add_button('Помощь', color=VkKeyboardColor.PRIMARY)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user = [vk.users.get(user_id=event.user_id)[0][x] for x in ["first_name", "last_name", "id"]]
            if event.from_user:
                print(f'{user[0]} {user[1]} (id{user[2]}) написал(а) в группу: {event.text}')
            elif event.from_chat:
                print(f'{user[0]} {user[1]} (id_{user[2]}) написал(а) в беседу: {event.text}')
            con = sqlite3.connect('db/mode.sqlite')
            cur = con.cursor()
            f = cur.execute("""SELECT type,ex FROM mode WHERE id = ?""", (user[2],)).fetchall()
            if not f or event.from_chat:
                text = event.text.lower()
                if text == 'таблица менделеева':
                    message('Лови табличку Менделеева', photos['tM'], 0)
                elif len(text) > 3 and text[:4] == 'реши':
                    if text[4:] != '' and text[4:] != ' ' and text[4] == ' ':
                        try:
                            par = parse(text[5:])
                            if par:
                                message(par, None, 0)
                            else:
                                message('Неверное уравнение', None, 0)
                        except:
                            message('Неверное уравнение', None, 0)
                    else:
                        message('Укажите уравнение', None, 0)
                elif text == 'таблица растворимости':
                    message('Лови табличку растворимости', photos['tR'], 0)
                elif text == 'ряд активности':
                    message('Лови ряд активности', photos['rA'], 0)
                elif text == 'свойства кислотных оксидов':
                    message(''.join(open(files['SVKO'], 'r', encoding='UTF-8').readlines()), None, 0)
                elif text == 'свойства основных оксидов':
                    message(''.join(open(files['SVOO'], 'r', encoding='UTF-8').readlines()), None, 0)
                elif text == 'свойства щелочей':
                    message(''.join(open(files['SVSch'], 'r', encoding='UTF-8').readlines()), None, 0)
                elif text == 'свойства нерастворимых оснований':
                    message(''.join(open(files['SVNO'], 'r', encoding='UTF-8').readlines()), None, 0)
                elif text == 'свойства кислот':
                    message(''.join(open(files['SVK'], 'r', encoding='UTF-8').readlines()), None, 0)
                elif text == 'свойства солей':
                    message(''.join(open(files['SVS'], 'r', encoding='UTF-8').readlines()), None, 0)
                elif 'задания' in text:
                    if event.from_user:
                        if event.text.lower() == 'задания':
                            message(''.join(open(files['EH'], 'r', encoding='UTF-8').readlines()), None, 0)
                        elif event.text.lower() == 'задания элементы':
                            message('Чтобы закончить напиши "Стоп".\nПоехали!', None, 0)
                            elem(user, atm)
                        elif event.text.lower() == 'задания кислоты':
                            message('Чтобы закончить напиши "Стоп".\nПоехали!', None, 0)
                            kisloti(user, kisl)
                        elif event.text.lower() == 'задания свойства оксидов':
                            message('Твоя задача закончить и уровнять реакцию.', None, 0)
                            message('Если реакция не идёт, после = пиши "-".', None, 0)
                            message('Чтобы закончить напиши "Стоп".\nПоехали!', None, 0)
                            svoistva(user, 1)
                        elif event.text.lower() == 'задания свойства кислот':
                            message('Твоя задача закончить и уровнять реакцию.', None, 0)
                            message('Если реакция не идёт, после = пиши "-".', None, 0)
                            message('Чтобы закончить напиши "Стоп".\nПоехали!', None, 0)
                            svoistva(user, 2)
                        elif event.text.lower() == 'задания свойства оснований':
                            message('Твоя задача закончить и уровнять реакцию.', None, 0)
                            message('Если реакция не идёт, после = пиши "-".', None, 0)
                            message('Чтобы закончить напиши "Стоп".\nПоехали!', None, 0)
                            svoistva(user, 4)
                        elif event.text.lower() == 'задания свойства солей':
                            message('Твоя задача закончить и уровнять реакцию.', None, 0)
                            message('Если реакция не идёт, после = пиши "-".', None, 0)
                            message('Чтобы закончить напиши "Стоп".\nПоехали!', None, 0)
                            svoistva(user, 3)
                        elif event.text.lower() == 'задания свойства':
                            message('Твоя задача закончить и уровнять реакцию.', None, 0)
                            message('Если реакция не идёт, после = пиши "-".', None, 0)
                            message('Чтобы закончить напиши "Стоп".\nПоехали!', None, 0)
                            svoistva(user, 0)
                        else:
                            message('Простите, я вас не понял. Для списка комманд напишите "Помощь"',
                                    None, hl.get_keyboard())
                    else:
                        message('Простите, но эта возможность работает только в личных сообщениях группы', None, 0)
                elif 'помощь' in event.text.lower().split(' ') :
                    message(''.join(open(files['H'], 'r', encoding='UTF-8').readlines()), None, 0)
                else:
                    message('Простите, я вас не понял. Для списка комманд напишите "Помощь"', None, hl.get_keyboard())
            elif f:
                if event.from_user:
                    f = list(f[0])
                    f[0] = cur.execute("""SELECT name FROM types WHERE id = ?""", (f[0],)).fetchone()[0]
                    o = f
                    if event.text.lower() == 'стоп':
                        cur.execute("""DELETE FROM mode WHERE id = ?""", (user[2],))
                        con.commit()
                        message('Ну что, чего теперь будем учить?', None, hl.get_keyboard())
                    elif event.text.lower() == 'дальше':
                        message('Хорошо, попробуй это.', None, 0)
                        if f[0][0] == 'A':
                            elem(user, atm)
                        if f[0][0] == 'K':
                            kisloti(user, kisl)
                        if f[0][0] == 'S':
                            svoistva(user, f[0][1])
                    elif sorted(event.text.lower().split(' ')) == sorted(o[1].lower().split(' ')):
                        message('Отлично! Продолжим...', None, 0)
                        if f[0][0] == 'A':
                            elem(user, atm)
                        if f[0][0] == 'K':
                            kisloti(user, kisl)
                        if f[0][0] == 'S':
                            svoistva(user, f[0][1])
                    else:
                        message('Не верный ответ, попробуй ещё!\nНапиши "Дальше" чтобы получить новое задание.', None, zad.get_keyboard())
                else:
                    message('Простите, но эта возможность работает только в личных сообщениях группы', None, 0)

def parse(react):
    react = react.replace('+', '+%2B+').replace('(', '%28').replace(')', '%29').replace(' ', '').replace('=', '+%3D+')
    response = requests.get(f'https://chemequations.com/ru/?s={react}&ref=input', headers={'User-Agent': UserAgent().chrome})
    response = response.content.decode('UTF-8')
    soup = str(BeautifulSoup(response, 'html.parser'))
    left = soup.find('<title>')
    right = soup[left:].find('Вычисл') - 3 + left
    return soup[left + 7:right]


def elem(user, atm):
    global zad
    con = sqlite3.connect('db/atoms.sqlite')
    cur = con.cursor()
    sp = ['elem', 'mass', 'num']
    dd = random.choice(sp)
    sp.remove(dd)
    oo = random.choice(sp)
    d = random.choice(list(map(lambda x: x[0], cur.execute(f"""SELECT {dd} FROM atoms""").fetchall())))
    o = cur.execute(f"""SELECT {oo} FROM atoms WHERE {dd} = ?""", (d,)).fetchone()[0]
    message(f'Назовите {atm[oo][0]} элемента, {atm[dd][1]} которого {d}', None, zad.get_keyboard())
    con = sqlite3.connect('db/mode.sqlite')
    cur = con.cursor()
    type = cur.execute(f'''SELECT id FROM types WHERE name = ?''', ("A" + oo,)).fetchone()[0]
    cur.execute(f"""INSERT INTO mode(id,type,ex) VALUES
                             (?, ?, ?) """, (user[2], type, o))
    con.commit()


def kisloti(user, kisl):
    global zad
    con = sqlite3.connect('db/kisloti.sqlite')
    cur = con.cursor()
    sp = ['form', 'name', 'ost']
    dd = random.choice(sp)
    sp.remove(dd)
    oo = random.choice(sp)
    d = random.choice(list(map(lambda x: x[0], cur.execute(f"""SELECT {dd} FROM kisloti""").fetchall())))
    o = cur.execute(f"""SELECT {oo} FROM kisloti WHERE {dd} = ?""", (d,)).fetchone()[0]
    message(f'Назовите {kisl[oo][0]} кислоты, {kisl[dd][1]} которой {d}', None, zad.get_keyboard())
    con = sqlite3.connect('db/mode.sqlite')
    cur = con.cursor()
    type = cur.execute(f'''SELECT id FROM types WHERE name = ?''', ("K" + oo,)).fetchone()[0]
    cur.execute(f"""INSERT INTO mode(id,type,ex) VALUES
                                 (?, ?, ?) """, (user[2], type, o))
    con.commit()


def svoistva(user, mode):
    global zad
    con = sqlite3.connect('db/react.sqlite')
    cur = con.cursor()
    if int(mode) != 0:
        d = random.choice(
            list(map(lambda x: x[0], cur.execute(f"""SELECT dano FROM uravn WHERE theme = ?""", (mode,)).fetchall())))
        o = cur.execute(f"""SELECT otvet FROM uravn WHERE dano = ?""", (d,)).fetchone()[0]
    else:
        d = random.choice(list(map(lambda x: x[0], cur.execute(f"""SELECT dano FROM uravn""").fetchall())))
        o = cur.execute(f"""SELECT otvet FROM uravn WHERE dano = ?""", (d,)).fetchone()[0]
    message(d.split('=')[0].strip() + ' =', None, zad.get_keyboard())
    con = sqlite3.connect('db/mode.sqlite')
    cur = con.cursor()
    type = cur.execute(f'''SELECT id FROM types WHERE name = ?''', ("S" + str(mode),)).fetchone()[0]
    cur.execute(f"""INSERT INTO mode(id,type,ex) VALUES
                                     (?, ?, ?) """, (user[2], type, o))
    con.commit()


def photo(links):
    global upload
    photos = list()
    for link in links:
        photo = upload.photo_messages(link)
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        photos.append(f'photo{owner_id}_{photo_id}_{access_key}')
    return photos


def message(mess, att, key):
    global event
    global keyboard
    global vk
    global zad
    if event.from_user:
        vk.messages.send(
            user_id=event.user_id,
            message=mess,
            random_id=0,
            attachment=att,
            keyboard=[key if key != 0 else None][0])
    elif event.from_chat:
        vk.messages.send(
            chat_id=event.chat_id,
            message=mess,
            random_id=0,
            attachment=att,
            keyboard=[key if key != 0 else None][0])


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


main()