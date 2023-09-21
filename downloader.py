import requests


def upload_to_telegraph(file_path):
	response = requests.post("https://telegra.ph/upload", files={"file": open(file_path, "rb")})

	if response.status_code == 200:
		result = response.json()
		if "src" in result[0]:
			return "https://telegra.ph" + result[0]["src"]

	return None
