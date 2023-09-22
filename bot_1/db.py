import aiosqlite


async def start_db():
	async with aiosqlite.connect("base.db") as db:
		cursor = await db.cursor()
		await cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Telegram_ID INTEGER,
                Telegram_Tag TEXT,
                Name TEXT,
                Age INTEGER,
                City TEXT
            )
        ''')
		await db.commit()


async def add_user(telegram_id, telegram_tag, name, age, city):
	async with aiosqlite.connect("base.db") as db:
		cursor = await db.cursor()
		await cursor.execute('''
            INSERT INTO Users (Telegram_ID, Telegram_Tag, Name, Age, City)
            VALUES (?, ?, ?, ?, ?)
        ''', (telegram_id, telegram_tag, name, age, city))
		await db.commit()


async def check_user(telegram_id):
	async with aiosqlite.connect("base.db") as db:
		cursor = await db.cursor()
		await cursor.execute('SELECT * FROM Users WHERE Telegram_ID = ?', (telegram_id,))
		user = await cursor.fetchone()
		return user is not None


async def del_user(telegram_id):
	async with aiosqlite.connect("base.db") as db:
		cursor = await db.cursor()
		await cursor.execute('DELETE FROM Users WHERE Telegram_ID = ?', (telegram_id,))
		await db.commit()


async def get_user(telegram_id):
	async with aiosqlite.connect("base.db") as db:
		cursor = await db.cursor()
		await cursor.execute('SELECT * FROM Users WHERE Telegram_ID = ?', (telegram_id,))
		user = await cursor.fetchone()
		return user
