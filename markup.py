from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btn_all = KeyboardButton('/watch')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_all)

