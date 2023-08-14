import datetime
import json
import telebot
from render_template import render_template

from config import TOKEN
from keyboards import main_keyboard, document_state_keyboard
from soap.connect_to_1c import get_soap_client

bot = telebot.TeleBot(TOKEN)

LOG_PATH = '../logs/bot_log.txt'

HELP = '''
Список доступных команд:
/help - вывести список доступных команд.
🚚 Вернуть рейс  - вернуть указанный рейс на проходную или в печать документов.
'''


def bot_send_message(chat_id, text, parse_mode=None, reply_markup=None):
    try:
        return bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)
    except Exception as ex:
        with open(LOG_PATH, 'a') as file_log:
            str_log = f'{datetime.datetime.now()} | chat_id: {chat_id} ex: {ex} \n'
            file_log.write(str_log)


@bot.message_handler(commands=['start'])
def start(message):
    soap_client = get_soap_client()
    text = soap_client.FindUser(message.chat.id)
    dict_rez = json.loads(text)
    if dict_rez["Status"] == 'Error':
        bot_send_message(message.chat.id,
                         f"{dict_rez['Text']} Сообщите свой ID {message.chat.id} в отдел ИТ для регистрации.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        send_message = f"<b>Приветствую, {dict_rez['Text']}</b>\nЧтобы выбрать действие, нажмите на нужную кнопку." \
                       f"Перезапуск бота команда: /start или очистите историю чата."
        bot_send_message(message.chat.id, send_message, parse_mode='html', reply_markup=main_keyboard)


@bot.message_handler(commands=["help"])
def send_help(message):
    text = f'<b>Приветствую, {message.chat.first_name}.</b>' + HELP
    bot_send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(func=lambda msg: msg.text == '🚚 Вернуть рейс')
def change_document_state(message):
    text = 'Введите номер рейса. Только цифры!'
    msg = bot_send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, process_doc_number)


def process_doc_number(message):
    doc_number = message.text

    if doc_number.isdigit():
        soap_client = get_soap_client()
        text = soap_client.DocumentState(doc_number)
        dict_rez = json.loads(text)
        if dict_rez["Status"] == 'Error':
            bot_send_message(message.chat.id, dict_rez['Text'], parse_mode='html', reply_markup=main_keyboard)
        else:
            doc_stat_dict = dict_rez['StateList']
            text = render_template("doc_state.html", doc_stat_dict=doc_stat_dict)
            msg = bot_send_message(message.chat.id, text, parse_mode='html', reply_markup=document_state_keyboard)
            bot.register_next_step_handler(msg, process_change_state, doc_number)
    else:
        text = 'Некорректный номер рейста. Введите номер рейса. Только цифры!'
        msg = bot_send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, process_doc_number)


def process_change_state(message, doc_number):
    state = ''
    if message.text == '🔚 ️Отмена':
        text = 'Рейс не изменен. Возврат в главное меню.'
        bot_send_message(message.chat.id, text, parse_mode='html', reply_markup=main_keyboard)
    elif message.text == '🖨️  Печать документов':
        state = 'Погрузка'
    elif message.text == '➡️Проходная':
        state = 'Проходная'

    if state:
        soap_client = get_soap_client()
        text = soap_client.ChangeDocumentState(state, doc_number)
        dict_rez = json.loads(text)
        if dict_rez["Status"] == 'Error':
            bot_send_message(message.chat.id, dict_rez['Text'], parse_mode='html', reply_markup=main_keyboard)
        else:
            doc_stat_dict = dict_rez['StateList']
            bot_send_message(message.chat.id, f'Успешно изменено состояние маршрута - {state}', parse_mode='html',
                             reply_markup=main_keyboard)
            text = render_template("doc_state.html", doc_stat_dict=doc_stat_dict)
            bot_send_message(message.chat.id, text, parse_mode='html', reply_markup=main_keyboard)


if __name__ == '__main__':
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
