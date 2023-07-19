import random
import urllib


def hello(event, context):
	# read url parameter 'w'
	w = event.get('queryStringParameters', {}).get('w', 0)

	# urldecode w
	w = urllib.parse.unquote(w)
	w = w.split("\n")
	high = w[0]
	low = w[1]
	condition = w[2]
	precipitation_amount = w[3]
	precipitation_chance = w[4]

	weather_type = ""

	if "cloudy" in condition.lower():
		weather_type = "cloudy"
	elif "drizzle" or "showers" in condition.lower():
		weather_type = "rainy"
	elif "foggy" in condition.lower():
		weather_type = "foggy"
	elif "windy" in condition.lower():
		weather_type = "windy"
	elif "thunderstorm" in condition.lower():
		weather_type = "thunderstorm"
	elif high > 80:
		weather_type = "hot"
	elif high < 40:
		weather_type = "cold"
	else:
		weather_type = "good"

	# read in all the filepaths from filepaths.txt
	with open("filepaths.txt", "r") as file:
		filepaths = file.read().split("\n")

	# filter for only the filepaths that match the weather type
	filepaths = [filepath for filepath in filepaths if weather_type in filepath]
	# choose a random filepath
	filepath = random.choice(filepaths)
	url = f"https://raw.githubusercontent.com/ExtraE113/leah_birthday/master/leah-birthday-image/{filepath}"
	print(url)
	# return temporary redirect to that url
	response = {
		"statusCode": 302,
		"headers": {
			"Location": url
		}
	}

	return response
