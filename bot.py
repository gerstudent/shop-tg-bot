import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker("CAACAgIAAxkBAAMGZKa_4SN7y425QV79kUw7GfMtYr0AAkIQAAIzxSlJkA7UEacqSoIvBA")
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин!')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Такой команды не существует')


@dp.message_handler(content_types=['sticker'])
async def check_stick(message: types.Message):
    await message.answer(message.sticker.file_id)
    await bot.send_message(message.from_user.id, message.chat.id)


@dp.message_handler(content_types=['photo', 'document'])
async def forward_file(message: types.Message):
    await bot.forward_message(os.getenv("GROUP_ID"), message.from_user.id, message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
