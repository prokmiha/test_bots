from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db import start_db, add_user, check_user, del_user, get_user

import logging
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class RegistrationStates(StatesGroup):
	waiting_for_name = State()
	waiting_for_age = State()
	waiting_for_city = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await start_db()
	telegram_id = message.from_user.id
	if not await check_user(telegram_id):
		await message.answer("Добро пожаловать! Давайте начнем анкетирование.\n\nВведите ваше имя:")
		await RegistrationStates.waiting_for_name.set()
	else:
		await message.answer("Вы уже зарегистрированы")


@dp.message_handler(state=RegistrationStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
	await message.answer("Сколько вам лет?")
	await RegistrationStates.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=RegistrationStates.waiting_for_age)
async def process_age_invalid(message: types.Message):
	await message.answer("Пожалуйста, введите возраст цифрами (пример: 25).")


@dp.message_handler(lambda message: message.text.isdigit(), state=RegistrationStates.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['age'] = int(message.text)
	await message.answer("В каком городе вы живете?")
	await RegistrationStates.next()


@dp.message_handler(state=RegistrationStates.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['city'] = message.text
		telegram_id = message.from_user.id
		await add_user(telegram_id, message.from_user.username, data['name'], data['age'], data['city'])
		await message.answer("Спасибо за регистрацию! Ваши данные сохранены.")
	await state.finish()


@dp.message_handler(commands=['deleteme'])
async def delete_me(message: types.Message):
	telegram_id = message.from_user.id
	if await check_user(telegram_id):
		await del_user(telegram_id)
		await message.answer("Ваш профиль удален.")
	else:
		await message.answer("Вы еще не зарегистрированы.")


@dp.message_handler(commands=['getme'])
async def get_me(message: types.Message):
	telegram_id = message.from_user.id
	user = await get_user(telegram_id)
	if user:
		user_info = f"ID: {user[0]}\nTelegram ID: {user[1]}\nTelegram Tag: {user[2]}\nName: {user[3]}\nAge: {user[4]}\nCity: {user[5]}"
		await message.answer(f"Ваши данные:\n\n{user_info}", parse_mode=ParseMode.MARKDOWN)
	else:
		await message.answer("Вы еще не зарегистрированы.")


if __name__ == '__main__':
	from aiogram import executor

	executor.start_polling(dp, skip_updates=True)
