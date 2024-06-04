from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_photo_names, get_general_catalog

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Добавить фото')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт')

photo_keyboad = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Изменить'), KeyboardButton(text='Удалить')],
    [KeyboardButton(text='Назад в меню')]

],
    resize_keyboard=True, input_field_placeholder='Выберите пункт')


async def create_photos_keyboard(user_id) -> InlineKeyboardMarkup:
    all_photos = await get_photo_names(user_id)
    keyboard = InlineKeyboardBuilder()
    if all_photos:
        for photo in all_photos:
            keyboard.add(InlineKeyboardButton(text=photo.name, callback_data=f'photo_{photo.id}'))
    return keyboard.adjust(2).as_markup()


async def create_general_photos_keyboard() -> InlineKeyboardMarkup:
    all_photos = await get_general_catalog()
    keyboard = InlineKeyboardBuilder()
    if all_photos:
        for photo in all_photos:
            keyboard.add(InlineKeyboardButton(text=photo.name, callback_data=f'photo_{photo.id}'))
    return keyboard.adjust(2).as_markup()


admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Общий каталог'), KeyboardButton(text='Отчистить каталог')],
    [KeyboardButton(text='Отправить рассылку')],
    [KeyboardButton(text='Назад в меню')]
], resize_keyboard=True)
