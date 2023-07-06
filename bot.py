import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Каталог', 'Корзина', 'Контакты']
keyboard.add(*buttons)

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb_buttons = ['Каталог', 'Корзина', 'Контакты', 'Админ-панель']
admin_kb.add(*admin_kb_buttons)

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel_buttons = ['Добавить товар', 'Удалить товар', 'Рассылка']
admin_panel.add(*admin_panel_buttons)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker("CAACAgIAAxkBAAMGZKa_4SN7y425QV79kUw7GfMtYr0AAkIQAAIzxSlJkA7UEacqSoIvBA")
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин!', reply_markup=keyboard)

    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await message.answer('Вы авторизовались как админ', reply_markup=admin_kb)


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Каталог')
async def contacts(message: types.Message):
    await message.answer('Каталог нашего магазина')


@dp.message_handler(text='Корзина')
async def contacts(message: types.Message):
    await message.answer('Корзина')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer('Контакты нашего магазина')


@dp.message_handler(text='Админ-панель')
async def admin_panel_handler(message: types.Message):
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await message.answer('Вы находитесь в админ-панели', reply_markup=admin_panel)
    else:
        await message.reply('Такой команды не существует')


@dp.message_handler(content_types=['sticker'])
async def check_stick(message: types.Message):
    await message.answer(message.sticker.file_id)
    await bot.send_message(message.from_user.id, message.chat.id)


@dp.message_handler(content_types=['photo', 'document'])
async def forward_file(message: types.Message):
    await bot.forward_message(os.getenv("GROUP_ID"), message.from_user.id, message.message_id)


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Такой команды не существует')


if __name__ == '__main__':
    executor.start_polling(dp)
