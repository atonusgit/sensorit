import os
import json
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()
logsfolder = os.getenv('ROOT_DIRECTORY') + "/sunrise_sunset_logs/"

def get_sunrise_sunset():
	response = requests.get("https://api.sunrise-sunset.org/json?lat=" + os.getenv('PUSULA_LAT') + "&lng=" + os.getenv('PUSULA_LNG') + "&date=today&formatted=0")
	return response.json()

def write_json(data, filename=datetime.datetime.now().strftime("%y%m%d") + '_sunrise_sunset.json'):
	with open(logsfolder + filename, 'w') as f:
		json.dump(data, f, indent=4)

def main():
	response = get_sunrise_sunset()
	write_json(response)

if __name__ == "__main__":
	main()
