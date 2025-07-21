from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from .keyboards import keyboard

router = Router()

@router.message(Command('start'))
async def say_hello(message: Message):
    await message.answer('Привет! Я бот для общения с нейросетью. Выберете действие:', reply_markup=keyboard)

@router.message(Command('roll_dice'))
async def dice(message: Message):
    await message.answer_dice()
