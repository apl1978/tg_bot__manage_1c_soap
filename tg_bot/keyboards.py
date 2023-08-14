from telebot import types

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
m_btn1 = types.KeyboardButton('/help')
m_btn2 = types.KeyboardButton('🚚 Вернуть рейс')
main_keyboard.add(m_btn1, m_btn2)

document_state_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
ds_btn1 = types.KeyboardButton('🖨️  Печать документов')
ds_btn2 = types.KeyboardButton('➡️Проходная')
ds_btn3 = types.KeyboardButton('🔚 ️Отмена')
document_state_keyboard.add(ds_btn1, ds_btn2, ds_btn3)
