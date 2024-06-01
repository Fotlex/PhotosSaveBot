from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_photo_names

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


async def create_photos_keyboard() -> InlineKeyboardMarkup:
    all_photos = await get_photo_names()
    keyboard = InlineKeyboardBuilder()
    if all_photos:
        for photo in all_photos:
            keyboard.add(InlineKeyboardButton(text=photo.name, callback_data=f'photo_{photo.id}'))
    return keyboard.adjust(2).as_markup()
