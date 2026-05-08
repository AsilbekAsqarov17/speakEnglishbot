import logging
import asyncio
from unittest import result
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from oxfordLookup import getDefinitions
from deep_translator import GoogleTranslator
from langdetect import detect

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm Translate bot by Voskar")

@dp.message(Command('help'))
async def send_help(message: types.Message):
    await message.reply("This bot can give you defintions and pronunciations of the word you type and text translation!")

@dp.message()
async def tarjimon(message: types.Message):

    if len(message.text.split()) > 2:

        try:
            translated_text = GoogleTranslator(source='auto', target='uz').translate(message.text)
            if translated_text.strip().lower() == message.text.strip().lower():
                translated_text = GoogleTranslator(source='auto', target='en').translate(message.text)

            await message.reply(translated_text)
        except Exception as e:
            logging.error(f"Translation Error {e}")
    else:
        lang = detect(message.text)
        if lang == 'en':
            word_id = message.text
        else:
            word_id = GoogleTranslator(source='uz', target='en').translate(message.text)
        lookup = getDefinitions(word_id)

        if lookup:
            await message.reply(f"Word: {word_id}\nDefinition: {lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Sorry, Could not find the word!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot turned off")