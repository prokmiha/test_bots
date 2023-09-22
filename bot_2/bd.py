import aiosqlite


async def create_db():
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.cursor()
		await cursor.execute('''
			CREATE TABLE IF NOT EXISTS Users(
				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				Random_Name TEXT,
				Random_Number INTEGER)
			''')
		await db.commit()


async def add_to_db(data):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.cursor()
		await cursor.execute('''
			INSERT INTO Users(Random_Name, Random_Number)
			VALUES (?, ?)
			''', data)
		await db.commit()


async def return_from_db(limit):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.cursor()
		await cursor.execute('''
			SELECT * FROM Users LIMIT ?
			''', (limit,))
		data = await cursor.fetchall()
		return data
