# coding=utf-8
import logging
import asyncio
from typing import Optional

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = 'YOURTOKEN'

# Expedition time dictionary
expedition_dict = {'1': 15, '2': 30, '3': 20, '4': 50, '5': 90, '6': 40, '7': 60, '8': 180, 'A1': 25, 'A2': 55,
                   'A3': 135,
                   '9': 240, '10': 90, '11': 300, '12': 480, '13': 240, '14': 360, '15': 720, '16': 900, 'B1': 35,
                   'B2': 520,
                   '17': 45, '18': 300, '19': 360, '20': 120, '21': 140, '22': 180, '23': 240, '24': 500,
                   '25': 2400, '26': 4800, '27': 1200, '28': 1500, '29': 1440, '30': 2880, '31': 120, '32': 1440,
                   '35': 420, '36': 540, '37': 165, '38': 175, '39': 1800, '40': 410}

# Configure logging
loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    id = State()
    expedition1 = State()
    expedition2 = State()
    expedition3 = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.id.set()
    await Form.expedition1.set()

    await message.reply("发送你的远征编号,每次请发送一个")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Canceled.', reply_markup=types.ReplyKeyboardRemove())


# Check the reply should be digits
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.expedition1)
async def failed_process_age(message: types.Message):
    """
    If it is invalid
    """
    return await message.reply("发送数字编号哦")


@dp.message_handler(state=Form.expedition1)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['e1'] = message.text
        data['id'] = message.chat.id
    await asyncio.sleep(expedition_dict[message.text]*60)
    await message.reply("收远征{}啦".format(message.text))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
