from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_2 import config
from bot_2.bd import create_db, add_to_db, return_from_db

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
process = False
user_data = []


class ReturnState(StatesGroup):
	limit = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await create_db()
	await message.answer("Отправь мне сообщения в формате 'текст число'. "
	                     "Когда закончишь, нажми /stop.")
	await message.answer("Или отправь /return для вывода данных из базы")


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
	for data in user_data:
		await add_to_db(data)
	await message.reply("Данные сохранены. Если хочешь начать заново, отправь /start.")
	user_data.clear()


@dp.message_handler(commands=['return'])
async def return_def(message: types.Message):
	await message.answer("Введите число, которым вы хотите ограничить вывод данных (от 1 до 10).")
	await ReturnState.limit.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=ReturnState.limit)
async def process_limit(message: types.Message, state: FSMContext):
	limit = int(message.text)
	result = await return_from_db(limit)
	final = '\n'.join([f"{item[0]}. {item[1]}: {item[2]}" for item in result])

	await message.answer(final)

	await state.finish()


@dp.message_handler(regexp=r'^[A-Za-z]+\s\d+$')
async def process_data(message: types.Message):
	data = message.text.split()
	user_data.append((data[0], int(data[1])))
	await message.answer(f"Данные '{data[0]}' и '{data[1]}' добавлены. Ожидаю следующее сообщение или /stop.")


if __name__ == '__main__':
	from aiogram import executor

	executor.start_polling(dp, skip_updates=True)
