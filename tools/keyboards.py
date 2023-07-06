from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Каталог', 'Корзина', 'Контакты']
keyboard.add(*buttons)

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb_buttons = ['Каталог', 'Корзина', 'Контакты', 'Админ-панель']
admin_kb.add(*admin_kb_buttons)

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel_buttons = ['Добавить товар', 'Удалить товар', 'Рассылка']
admin_panel.add(*admin_panel_buttons)

catalog_kb = InlineKeyboardMarkup()
catalog_kb.add(InlineKeyboardButton(text='Товар 1', callback_data='item 1'),
               InlineKeyboardButton(text='Товар 2', callback_data='item 2'),
               InlineKeyboardButton(text='Товар 3', callback_data='item 3')
               )
