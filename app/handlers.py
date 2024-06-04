import os

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.database.requests as rq
import app.keyboards as kb
import app.states as st

router = Router()

current_photo_name = []
current_photo_id = []


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer('Привет!', reply_markup=kb.main_keyboard)


@router.message(Command('admin'))
async def open_admin_panel(message: Message, state: FSMContext) -> None:
    if str(message.from_user.id) == os.getenv('ADMIN_ID'):
        await message.answer('Админ панель', reply_markup=kb.admin_keyboard)
        await state.set_state(st.States.admin_state)
    else:
        await message.answer(f'У вас недостаточно прав {message.from_user.id}, {os.getenv('ADMIN_ID')}', reply_markup=kb.main_keyboard)


@router.message(F.text == 'Общий каталог', st.States.admin_state)
async def open_general_catalog(message: Message) -> None:
    await message.answer('Общий каталог', reply_markup=await kb.create_general_photos_keyboard())


@router.message(F.text == 'Отчистить каталог', st.States.admin_state)
async def clear_database(message: Message, state: FSMContext) -> None:
    await rq.delete_all_photo()
    await message.answer('База данных отчищена', reply_markup=kb.admin_keyboard)
    await state.set_state(st.States.default_state)


@router.message(F.text == 'Назад в меню',)
async def back_to_menu(message: Message) -> None:
    await message.answer('Меню', reply_markup=kb.main_keyboard)


@router.message(F.text == 'Каталог')
async def open_catalog(message: Message) -> None:
    await message.answer('Каталог', reply_markup=await kb.create_photos_keyboard(
        message.from_user.id
    ))


@router.callback_query(F.data.startswith('photo_'))
async def open_photo(callback: CallbackQuery) -> None:
    photo_id = int(callback.data.split('_')[1])
    photo_file_id = await rq.get_photo_to_id(photo_id)
    current_photo_id.clear()
    current_photo_id.append(photo_id)
    await callback.message.answer_photo(photo=photo_file_id, reply_markup=kb.photo_keyboad)
    await callback.answer('Отправлено')


@router.message(F.text == 'Добавить фото')
async def add_photo(message: Message, state: FSMContext) -> None:
    await state.set_state(st.States.waiting_for_name)
    await message.answer('Придумайте название для фото')


@router.message(st.States.waiting_for_name, F.text)
async def set_name(message: Message, state: FSMContext) -> None:
    current_photo_name.append(message.text)
    await message.answer('Отправьте фото')
    await state.set_state(st.States.waiting_for_photo)


@router.message(st.States.waiting_for_photo, F.photo)
async def save_photo(message: Message) -> None:
    photo_data = message.photo[-1]
    await rq.set_photo(photo_data.file_id, current_photo_name[0], message.from_user.id)
    current_photo_name.clear()
    await message.answer('Успешно загружено', reply_markup=kb.main_keyboard)


@router.message(F.text == 'Изменить')
async def start_rename_photo(message: Message, state: FSMContext) -> None:
    await message.answer('Введите новое имя')
    await state.set_state(st.States.waiting_for_rename)


@router.message(st.States.waiting_for_rename, F.text)
async def rename_photo(message: Message, state: FSMContext) -> None:
    await rq.rename_photo(message.text, current_photo_id[0])
    await message.answer('Фото успешно переименовано', reply_markup=kb.photo_keyboad)
    await state.set_state(st.States.default_state)


@router.message(F.text == 'Удалить')
async def delete_photo(message: Message) -> None:
    await rq.delete_photo(current_photo_id[0])
    await message.answer('Фото удалено', reply_markup=kb.main_keyboard)
