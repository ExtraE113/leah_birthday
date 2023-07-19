import base64
import os
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

	# pick random image from the folder corresponding to the weather type
	# 1. get the list of files in the folder
	files = os.listdir("./" + weather_type)
	# 2. pick a random file
	file = random.choice(files)
	# 3. open the file & base64 encode it
	with open("./" + weather_type + "/" + file, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())

	response = {
		"statusCode": 200,
		"headers": {
			'Content-Type': 'image/png'
		},
		"body": encoded_string,
		"isBase64Encoded": True
	}

	return response
