import logging
from aiogram import Bot
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PhotoSize
from fsm.fsm import FSMStyleGen

user_router = Router()
logger = logging.getLogger(__name__)


@user_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text='Этот бот демонстрирует работу StyleGen\n\n'
             'Отправьте две фотографии'
    )

    await state.set_state(FSMStyleGen.send_photo)


@user_router.message(CommandStart())
async def process_wrong_start_command(message: Message):
    await message.answer(
        text='Бот уже запущен! Отправьте две фотографии или нажмите /cancel\n\n'
    )


@user_router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(
        text='Вы сбросили состояние бота.\n\n'
             'Чтобы начать заново, введите /start'
    )

    await state.clear()


@user_router.message(Command(commands="cancel"))
async def process_wrong_cancel_command(message: Message):
    await message.answer(
        text='Бот уже находится в начальном состоянии\n\n'
             'Чтобы начать пользоваться, введите /start'
    )


@user_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        text='Бот предназначен для генерации изображения определенного стиля\n\n'
             'Чтобы начать пользоваться, введите /start'
    )


@user_router.message(F.photo[-1].as_('largest_photo'), StateFilter(FSMStyleGen.send_photo))
async def process_photo_command(message: Message, largest_photo: PhotoSize, state: FSMContext, bot: Bot, photo_num: dict):

    file = await bot.get_file(largest_photo.file_id)

    if photo_num["photo_num"] == 0:
        logger.debug("first photo")
        photo_name = "style.jpg"
        photo_num["photo_num"] += 1
    else:
        logger.debug("second photo")
        photo_name = "content.jpg"
        photo_num["photo_num"] = 0

    await bot.download_file(file.file_path, photo_name)
    await state.set_state(FSMStyleGen.waiting_for_network)





# @user_router.message(F.photo[-1].as_('largest_photo'), StateFilter(FSMStyleGen.second_photo))
# async def process_start_command(message: Message, largest_photo: PhotoSize, state: FSMContext):
#     logger.debug("Second photo handler")
#     await state.clear()