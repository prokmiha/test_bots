import aiohttp

import config


async def telegraph_upload(bot, file):
	try:
		file_id = file["document"]["file_id"]
		file_name = file["document"]["file_name"]
		if not file.document.mime_type.split('/')[1].upper() in config.ALLOWED_FORMAT:
			return "Используйте файл нужного формата"

		file_info = await bot.get_file(file_id)
		print(file_info)

		file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_info.file_path}"

		async with aiohttp.ClientSession() as session:
			async with session.get(file_url) as response:
				if response.status == 200:
					file_bytes = await response.read()

			data = aiohttp.FormData()
			data.add_field(file_name, file_bytes)

			async with session.post("https://telegra.ph/upload", data=data) as response:
				if response.status == 200:
					result = await response.json()
					if "src" in result[0]:
						return "https://telegra.ph" + result[0]["src"]
		return "Произошла ошибка при загрузке контента."

	except Exception as e:
		print("An error occurred:", str(e))
