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

    await state.set_state(FSMStyleGen.first_photo)


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Бот уже запущен! Отправьте две фотографии или нажмите /cancel\n\n'
    )


@user_router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text='Вы сбросили состояние бота.\n\n'
             'Чтобы начать заново, введите /start'
    )

    await state.clear()


@user_router.message(Command(commands="cancel"))
async def process_start_command(message: Message):
    await message.answer(
        text='Бот уже находится в начальном состоянии\n\n'
             'Чтобы начать пользоваться, введите /start'
    )


@user_router.message(Command(commands="help"))
async def process_start_command(message: Message):
    await message.answer(
        text='Бот предназначен для генерации изображения определенного стиля\n\n'
             'Чтобы начать пользоваться, введите /start'
    )


@user_router.message(F.photo[-1].as_('largest_photo'), StateFilter(FSMStyleGen.first_photo))
async def process_start_command(message: Message, largest_photo: PhotoSize, state: FSMContext, bot: Bot):
    await state.set_state(FSMStyleGen.second_photo)
    logger.debug("First photo handler")
    file = await bot.get_file(largest_photo.file_id)
    print(file.file_path)
    await bot.download_file(file.file_path, "temp.jpg")



@user_router.message(F.photo[-1].as_('largest_photo'), StateFilter(FSMStyleGen.second_photo))
async def process_start_command(message: Message, largest_photo: PhotoSize, state: FSMContext):
    logger.debug("Second photo handler")
    await state.clear()