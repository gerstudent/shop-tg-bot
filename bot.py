import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин!')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Такой команды не существует')


if __name__ == '__main__':
    executor.start_polling(dp)
