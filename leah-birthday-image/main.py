# Importing the PIL library
import os
import shutil

from PIL import Image, ImageFont
from PIL import ImageDraw

# Open an Image
img = Image.open('base.png')

# Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(img)

# get image size
width, height = img.size

h_text_center = width / 2
v_text_center = height / 3

# open all files in './poems' and read each one to a string inside a dictionary
# skip file if it contains '_in' in its name
categories = {}
for filename in os.listdir("./poems"):
	if "_in" in filename or ".py" in filename:
		continue
	# specify encoding to avoid incorrect characters
	with open("./poems/" + filename, "r", encoding='UTF-8') as file:
		categories[filename] = file.read()

count = 0

# delete imgs
shutil.rmtree("imgs")
os.mkdir("imgs")

for item in categories:
	poems = categories[item].split("===")

	# create a folder for each category
	os.mkdir(f"imgs/{item.split('.')[0]}")

	for poem in poems:
		# Open an Image
		img = Image.open('base.png')

		# Call draw Method to add 2D graphics in an image
		I1 = ImageDraw.Draw(img)

		# check for lines that are too long
		#  max length should be X characters
		#  other lines should be split into multiple lines, second line indented 4 spaces
		lines = poem.split("\n")
		for i in range(len(lines)):
			if len(lines[i]) > 30:
				# find the first word before the 23rd character
				lines[i].split()
				split_index = 0
				for j in range(23, 0, -1):
					if lines[i][j] == " ":
						split_index = j
						break
				# split the line into two lines
				lines[i] = lines[i][:split_index] + "\n    " + lines[i][split_index + 1:]
		poem = "\n".join(lines)
		# print(poem)

		# Draw the text centered at (h_text_center, v_text_center) sized to have letters 5% of the image's height
		I1.multiline_text((h_text_center, v_text_center), poem, fill="black", anchor='ma',
						  font=ImageFont.truetype("arial.ttf", int(height * 0.03)))

		# Save the edited image
		img.save(f"imgs/{item.split('.')[0]}/edited{count}.png")
		count += 1
