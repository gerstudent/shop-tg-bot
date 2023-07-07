import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from tools import keyboards as kbs, db

load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_create()
    print('Бот запущен')


class Product(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Greet the user and display the admin keyboard if it is an admin

    Args:
        message: (types.Message) message from the user

    Returns:
        - Answer to keyword "/start" with text and sticker
        - Check the user id and if it is an admin id, shows the admin keyboard.

    """
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker(os.getenv("STICKER"))
    await message.answer(
        f'{message.from_user.first_name}, добро пожаловать в магазин!',
        reply_markup=kbs.keyboard
    )

    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await message.answer(
            'Вы авторизовались как админ', reply_markup=kbs.admin_kb
        )


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer('Каталог нашего магазина', reply_markup=kbs.catalog_kb)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer('Корзина')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer('Контакты нашего магазина')


@dp.message_handler(text='Админ-панель')
async def admin_panel_handler(message: types.Message):
    """Show admin panel

    Args:
        message: (types.Message) message from the user

    Returns:
        - Admin panel if user id is equal to admin id,
        else reply 'Такой команды не существует'

    """
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await message.answer(
            'Вы находитесь в админ-панели', reply_markup=kbs.admin_panel
        )
    else:
        await message.reply('Такой команды не существует')


@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    """Add item to a cart

    Args:
        message: (types.Message) message from the user

    Returns:
        - Catalog keyboard if product exists in database,
        else reply 'Такой команды не существует'

    """
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await Product.type.set()
        await message.answer('Выберите тип товара', reply_markup=kbs.catalog_kb)
    else:
        await message.reply('Такой команды не существует')


@dp.callback_query_handler(state=Product.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Введите название товара', reply_markup=kbs.cancel)
    await Product.next()


@dp.message_handler(state=Product.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Введите описание товара')
    await Product.next()


@dp.message_handler(state=Product.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Введите цену товара')
    await Product.next()


@dp.message_handler(state=Product.price)
async def add_item_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фотографию товара')
    await Product.next()


@dp.message_handler(lambda message: not message.photo, state=Product.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Сообщение не является фотографией')


@dp.message_handler(content_types=['photo'], state=Product.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Товар создан', reply_markup=kbs.admin_panel)
    await state.finish()


@dp.message_handler(content_types=['photo', 'document'])
async def forward_file(message: types.Message):
    await bot.forward_message(os.getenv("GROUP_ID"), message.from_user.id, message.message_id)


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 'item 1':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Ваш выбор: item 1')
    elif callback_query.data == 'item 2':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Ваш выбор: item 2')
    elif callback_query.data == 'item 3':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Ваш выбор: item 3')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Такой команды не существует')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
