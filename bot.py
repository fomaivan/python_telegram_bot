import requests
from aiogram import Bot, types, Dispatcher, executor
import markup
import logic_bot
import config

bot = Bot(token=config.my_token)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_command_func(message: types.Message):
    result = logic_bot.start(message)
    await bot.send_message(message.chat.id, result,
                           reply_markup=markup.main_menu, parse_mode="Markdown")


@dp.message_handler(commands='help')
async def help_command_func(message: types.Message):
    result = logic_bot.help_command()
    await bot.send_message(message.chat.id, result, parse_mode='Markdown')


@dp.message_handler(commands='add')
async def add_command_func(message: types.Message):
    result = logic_bot.add(message.chat.id, (message.text[5:].upper()))
    await bot.send_message(message.chat.id, result)


@dp.message_handler(commands='watch')
async def check_func(message: types.Message):
    await bot.send_message(message.chat.id, "Одну секунду ...")
    try:
        result = logic_bot.all(message.chat.id)
        await bot.send_message(message.chat.id, result, parse_mode='Markdown')
    except requests.exceptions.ConnectionError:
        await bot.send_message(message.chat.id, "Что то пошло не так... \n"
                                                "Попробуйте отправить свой запрос через некоторое время")


@dp.message_handler(commands='del')
async def del_func(message: types.Message):
    result = logic_bot.delete(message.chat.id, message.text[5:].upper())
    await bot.send_message(message.chat.id, result)

if __name__ == '__main__':
    executor.start_polling(dp)
