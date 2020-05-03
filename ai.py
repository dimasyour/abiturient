#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import re
import time
import random
import vk_api
import apiai, json
from vk_api.longpoll import *

from dbworker import *
from keyboard import *
from func import *

logging.basicConfig(filename="vkbot.log", level=logging.INFO)
logging.info("Start AbituentBotVk! " + str(datetime.now()))

token = os.environ.get('TOKEN_ABITUR')
vk_session = vk_api.VkApi(token=token)

global Random


def random_chat_id():
    chat_id = 0
    chat_id += random.randint(0, 1000000000)
    return chat_id

ans = Constants

def ais(msg):
    request = apiai.ApiAI('0a87568e576f41b5a25a238766958430').text_request() # Токен API к DialogFlow
    request.lang = 'ru' # Язык
    request.query = msg # Посылаем сообщение в DialogFlow                    
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON
    print(response)

def main():
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            vk = vk_session.get_api()
            print('Соединение установлено...')
            parse_html_html()
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text.lower()
                    ais(msg)
                    if not check_if_exists(event.user_id):
                        # получаем данные о пользователе (vk.com/dev/users.get)
                        user_data = vk.users.get(user_ids=event.user_id,
                                                 fields="last_name, firstname, sex, country, city, domain, photo_200")
                        UserID = user_data[0]["id"]
                        UserLastName = user_data[0]["last_name"]
                        UserFirstName = user_data[0]["first_name"]
                        UserSex = user_data[0]["sex"]
                        UserCountry = user_data[0]["country"]['title']
                        UserCity = user_data[0]["city"]['title']
                        UserDomain = user_data[0]["domain"]
                        UserPhoto200 = user_data[0]["photo_200"]
                        register_new_user(UserID, UserLastName, UserFirstName, UserSex, UserCountry, UserCity,
                                          UserDomain, UserPhoto200)

                    if msg in ('/start', 'начать', '📖 вернуться назад', 'назад к главной'):
                        vk.messages.send(
                            user_id=event.user_id,
                            message="Бот работает!",
                            keyboard=keyboard_start(),
                            random_id=random_chat_id()
                        )
                    elif msg in ('/my_ball', '📖 мои баллы'):
                        if get_status_ball(event.user_id):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="✅ Все ваши баллы указанны ниже: ",
                                keyboard=keyboard_subject_1(),
                                random_id=random_chat_id()
                            )
                            myballs = get_my_ball(event.user_id)
                            for i in range(len(myballs)):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=myballs[i],
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="⚠ Вы не добавили баллы!",
                                keyboard=keyboard_add_ball(),
                                random_id=random_chat_id()
                            )
                    elif msg in ('/add_ball', '📖 добавить баллы', 'показать предыдущие предметы'):
                        if get_status_ball(event.user_id):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="✅ Все ваши баллы указанны ниже: ",
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                            myballs = get_my_ball(event.user_id)
                            for i in range(len(myballs)):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=myballs[i],
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Выберите предмет, который хотите добавить!",
                                keyboard=keyboard_add_ball(),
                                random_id=random_chat_id()
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Выберите предмет, который хотите добавить!",
                                keyboard=keyboard_subject_1(),
                                random_id=random_chat_id()
                            )
                    elif msg in ('/add_ball_2', '📖 добавить баллы 2', 'показать следующие предметы'):
                        if get_user_ball_status(event.user_id) == 1:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="Ваши баллы: ",
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Выберите предмет, который хотите добавить!",
                                keyboard=keyboard_subject_2(),
                                random_id=random_chat_id()
                            )
                    elif event.text in (
                            '🧮 Профильная математика', '🇷🇺 Русский язык', '🏘 Обществознание', '🧬 Биология',
                            '⚛ Физика',
                            '🏰 История', '💻 Информатика', '🧪 Химия', '📝 Литература', '🗺 География'):
                        if event.text == '🧮 Профильная математика':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🧮 Введите количество баллов по Профильной математике: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 1)
                        elif event.text == '🇷🇺 Русский язык':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🇷🇺 Введите количество баллов по Русскому языку: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 2)
                        elif event.text == '🏘 Обществознание':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🏘 Введите количество баллов по Обществознанию: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 3)
                        elif event.text == '🧬 Биология':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🧬 Введите количество баллов по Биологии: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 4)
                        elif event.text == '⚛ Физика':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="⚛ Введите количество баллов по Физике: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 5)
                        elif event.text == '🏰 История':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🏰 Введите количество баллов по Истории: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 6)
                        elif event.text == '💻 Информатика':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="💻 Введите количество баллов по Информатике: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 7)
                        elif event.text == '🧪 Химия':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🧪 Введите количество баллов по Химии: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 8)
                        elif event.text == '📝 Литература':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="📝 Введите количество баллов по Литературе: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 9)
                        elif event.text == '🗺 География':
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🗺 Введите количество баллов по Географии: ",
                                keyboard=keyboard_insert_ball(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 10)
                    elif msg in ('/back_to_add_ball', '📖 назад к выбору предмета', 'отмена добавления балла'):
                        set_user_choose_subject(event.user_id, 0)
                        if get_user_ball_status(event.user_id) == 1:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="Ваши баллы: ",
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Выберите предмет, который хотите добавить!",
                                keyboard=keyboard_subject_1(),
                                random_id=random_chat_id()
                            )
                    elif (re.match(r"\d\d", event.text)) or (re.match(r"\d\d\d", event.text)):
                        set_user_ball(event.user_id, get_user_choose_subject(event.user_id), event.text)
                        vk.messages.send(
                            user_id=event.user_id,
                            message="🔰Вы ввели: " + event.text + "\n✔Баллы по предмету обновлены!",
                            keyboard=keyboard_start(),
                            random_id=random_chat_id()
                        )
                        set_user_choose_subject(event.user_id, 0)
                    elif msg in ('/remove_ball_to_choose_subject', '📖 удалить баллы по этому предмету'):
                        set_user_ball(event.user_id, get_user_choose_subject(event.user_id), 0)
                        if get_status_ball(event.user_id):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="✔Баллы у предмета удалены!",
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                            myballs = get_my_ball(event.user_id)
                            for i in range(len(myballs)):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=myballs[i],
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Выберите предмет, который хотите добавить!",
                                keyboard=keyboard_subject_1(),
                                random_id=random_chat_id()
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="✔Баллы у предмета удалены!\nБольше баллов нет. Добавьте их!",
                                keyboard=keyboard_subject_1(),
                                random_id=random_chat_id()
                            )
                    elif msg in ('/view_spec', '📖 направления и специальности', 'показать специальности'):
                        vk.messages.send(
                            user_id=event.user_id,
                            message="📒Выберите форму обучения: ",
                            keyboard=keyboard_spec(),
                            random_id=random_chat_id()
                        )
                    elif msg in ('/spec_och', '📒 очная', 'очная'):
                        vk.messages.send(
                            user_id=event.user_id,
                            message="⚠ Все специальности и направления\nочной формы обучения\n ниже: ",
                            keyboard=keyboard_spec(),
                            random_id=random_chat_id()
                        )
                        vk.messages.send(
                            user_id=event.user_id,
                            message=view_spec_och(),
                            keyboard=keyboard_spec(),
                            random_id=random_chat_id()
                        )
                    elif msg in ('/spec_zaoch', '📒 заочная', 'заочная'):
                        vk.messages.send(
                            user_id=event.user_id,
                            message="⚠ Все специальности и направления\nзаочной формы обучения\n ниже: ",
                            keyboard=keyboard_spec(),
                            random_id=random_chat_id()
                        )
                        vk.messages.send(
                            user_id=event.user_id,
                            message=view_spec(),
                            keyboard=keyboard_spec(),
                            random_id=random_chat_id()
                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            message="Неизвестная команда",
                            keyboard=keyboard_start(),
                            random_id=random_chat_id()
                        )
        except Exception as e:
            logging.error(str(datetime.now()) + " " + str(e))
            time.sleep(10)


if __name__ == '__main__':
    main()
