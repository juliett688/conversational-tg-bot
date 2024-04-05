import telebot # сама библиотека telebot
import time # необходим для cрока /mute и автоматического размута после срока мута
from random import choice

from telebot import custom_filters
from telebot import types

from config import token
from text_analysis import recognition_of_insults, get_emotion


import uuid
import os

from functions import convert_text_to_voice, recognise, translate_from_en_to_ru, detect


bot = telebot.TeleBot(token) # в TOKEN мы вводим непосредственно сам полученный токен.




@bot.chat_join_request_handler()
def make_some(message: telebot.types.ChatJoinRequest):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

# analys COMMANDS -------------------------------------------------------------------------------------------------------------------------------





@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы узнать, что я умею.")



@bot.message_handler(is_admin=True, commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно кикнуть администратора.")
        else:
            try:
                bot.ban_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был кикнут.")
            except:
                print("непредвиденная ошибка")
                bot.reply_to(message, f"Что-то пошло не так")
            
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")



@bot.message_handler(commands=['kick'])
def kick_user(message):
    bot.reply_to(message, f"Ха-ха тебе нельзя никого кикать")



@bot.message_handler(commands=['voice'])
def convert_text(message):
    if message.reply_to_message:
        try:
            path = convert_text_to_voice(message.reply_to_message.text)
            bot.send_chat_action(message.chat.id, 'record_voice', timeout=10)
            bot.send_voice(message.chat.id, open(f'{path}', 'rb'))
            os.remove(path=path) 
        except:
            bot.send_voice(message.chat.id, open('voices/sorry.mp3', 'rb'))

@bot.message_handler(commands=['emotion'])
def get_emotion_from_mes(message):
    if message.reply_to_message:
        print("cool")
        mes = get_emotion(message.text)
        bot.reply_to(message, f"{message.from_user.first_name} {mes}")
    else:
        print("HHhhhhhhhhhhhh")
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")





# analys TEXT FILTER ---------------------------------------------------------------------------------------------------------------------




@bot.message_handler(text_startswith=('Прив',"прив", "хай","Хай", "Бот", "бот"))
def text_filter(message):
    bot.reply_to(message, "Hi, {name}!".format(name=message.from_user.first_name))

@bot.message_handler(text_startswith=('Ахах',"ахах", "хаха", "Хах", "лол", "ржу", "ору"))
def text_filter(message):
    bot.reply_to(message, f"@{message.from_user.username} смешно тебе, да????")
    bot.reply_to(message, "😂")
 
@bot.message_handler(text_startswith=("Как дел", "как дел","Как ты", "как ты","ты как", "Ты как" ))
def text_filter(message):
    mood = choice(['Хорошо, ты как?', "Отстать, мне плохо", "Я так счастлив! надеюсь ты тоже", "На улице осень, на душе печаль, может попьем чай?"])
    bot.reply_to(message, f"{mood}")

@bot.message_handler(text_startswith=("ЧД", "чд","что дел", "че дел","Что дел", "Че дел" ))
def text_filter(message):
    mood = choice([
        "Я работаю над своим проектом",
        "Планирую свой день",
        "Изучаю что-то новое.",
        "Отдыхаю и развлекаюсь.",
        "Встречаюсь с друзьями",
        "Занимаюсь спортом",
        "Смотрю фильмы",
        "Играю в настольные игры.",
        "Путешествую",
        "Работаю над саморазвитием и личным ростом."
    ])
    bot.reply_to(message, f"{mood}")






# analys CONTENT TYPE ---------------------------------------------------------------------------------------------------------------------


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"

    file_info = bot.get_file(message.voice.file_id)

    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recognise(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)



@bot.message_handler(content_types=['photo'])
def photo_detection(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    path = "photos/"+str(uuid.uuid4()) +'.jpg'

    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    names, percent = detect(path)
    names = list(map(lambda name: translate_from_en_to_ru(name),names))
    
    bot.reply_to(message, f"Я думаю, что тут {names[0]} с вероятность {percent}%")
    
    bot.send_message(message.chat.id, f"Но также на фото может быть: {names[1]},{names[2]} или {names[3]}")
    os.remove(path)

# analys FUNCTIONS ---------------------------------------------------------------------------------------------------------------------



# filter on a specific message
@bot.message_handler(func=lambda message: "бот" in message.text.lower() )
def command_text_hi(m):
    bot.reply_to(m, "О ты обо мне?)))")





# analys ANOTHER MESSAGES ---------------------------------------------------------------------------------------------------------------------



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # проверяем сообщение на наличие запрещенных слов
    if recognition_of_insults(message.text):
        voice = choice(['insult.m4a',"ins2.m4a", "ins3.m4a" ])
        #bot.reply_to(message, f"@{message.from_user.username} Эй ! Ты что попутал! Тут нельзя ругаться!")
        bot.send_chat_action(message.chat.id, 'record_voice', timeout=6)
        bot.send_voice(message.chat.id, open(f'voices/{voice}', 'rb'))
    else:
        # если запрещенных слов нет, обрабатываем сообщение дальше
        print(message.text)









bot.add_custom_filter(custom_filters.IsReplyFilter())
bot.add_custom_filter(custom_filters.ForwardFilter())
bot.add_custom_filter(custom_filters.TextStartsFilter())
bot.infinity_polling(allowed_updates=telebot.util.update_types)
#bot.infinity_polling(none_stop=True)

"""
Метод bot.infinity_polling() является альтернативой методу bot.polling() и запускает бота в режиме бесконечного ожидания новых сообщений. Это значит, что бот будет постоянно проверять наличие новых сообщений и обрабатывать их. Параметр none_stop=True указывает на то, что бот будет продолжать работать даже в случае ошибок или проблем с подключением. Это важно, чтобы бот всегда был доступен для пользователей и мог обрабатывать их запросы.
"""
