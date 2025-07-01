import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from deep_translator import GoogleTranslator

import os
API_TOKEN = os.getenv("BOT_TOKEN")

user_langs = {}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
    "Привет! Я — бот-переводчик.\n"
    "Чтобы начать, выбери язык, на который я буду переводить твои сообщения.\n"
    "Для смены языка используй команду:\n"
    "/change"
)

@dp.message(Command('change'))
async def change_command(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="kk"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
            ],
            [
                InlineKeyboardButton(text="🇬🇧 English", callback_data="en"),
                InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="de"),
            ],
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uz"),
                InlineKeyboardButton(text="🇨🇳 中文", callback_data="zh-CN"),
            ],
            [
                InlineKeyboardButton(text="🇰🇷 한국어", callback_data="ko"),
                InlineKeyboardButton(text="🇪🇸 Español", callback_data="es"),
            ]
        ]
    )
    await message.answer("Выберите язык для перевода:", reply_markup=keyboard)


@dp.callback_query(F.data.in_(['kk', 'ru', 'en', 'de', 'uz', 'zh-CN', 'ko', 'es']))
async def set_language(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_langs[user_id] = callback.data
    await callback.message.edit_text(f"✅Перевод будет выполняться на: {callback.data.upper()}")
    await callback.answer()

@dp.message(F.text)
async def translate_text(message: Message):
    user_id = message.from_user.id
    target_lang = user_langs.get(user_id, 'en')
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
        await message.answer(f"Перевод ({target_lang}):\n{translated}")
    except Exception as e:
        await message.answer(f"❌ Ошибка при переводе:\n{e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
