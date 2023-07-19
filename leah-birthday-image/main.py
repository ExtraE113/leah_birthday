# Importing the PIL library
import os
import shutil
from tqdm import tqdm
from PIL import Image, ImageFont
from PIL import ImageDraw

PRODUCTION_RUN = True

# Open an Image
img = Image.open('base.jpg')

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

if PRODUCTION_RUN:
	# delete imgs
	shutil.rmtree("imgs")
	os.mkdir("imgs")

filepaths = []

for item in tqdm(categories):
	poems = categories[item].split("===")
	if PRODUCTION_RUN:
		# create a folder for each category
		os.mkdir(f"imgs/{item.split('.')[0]}")

	for poem in poems:
		# Open an Image
		img = Image.open('base_old.png')

		# Call draw Method to add 2D graphics in an image
		I1 = ImageDraw.Draw(img, "RGBA")

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

		grey = 10
		bbox = I1.textbbox((h_text_center, v_text_center), poem,
						   font=ImageFont.truetype("arial.ttf", int(height * 0.03)), anchor="ma")
		I1.rectangle(bbox, fill=(255 - grey, 255 - grey, 255 - grey, 25))

		# having drawn the background that covers the actual text, add a 40 px border on each side blending out to transparent
		# this is to hide the edges of the background
		# top
		size = 100
		# calculate factor such that the alpha value of the border is 0 at the edge of the background
		factor = 25 / size
		for i in range(size):
			I1.rectangle((bbox[0] - i, bbox[1] - i, bbox[2] + i, bbox[1] - i),
						 fill=(255 - grey, 255 - grey, 255 - grey, 25 - int(i * factor)))
		# bottom
		for i in range(size):
			I1.rectangle((bbox[0] - i, bbox[3] + i, bbox[2] + i, bbox[3] + i),
						 fill=(255 - grey, 255 - grey, 255 - grey, 25 - int(i * factor)))
		# left
		for i in range(size):
			I1.rectangle((bbox[0] - i, bbox[1] - i, bbox[0] - i, bbox[3] + i),
						 fill=(255 - grey, 255 - grey, 255 - grey, 25 - int(i * factor)))
		# right
		for i in range(size):
			I1.rectangle((bbox[2] + i, bbox[1] - i, bbox[2] + i, bbox[3] + i),
						 fill=(255 - grey, 255 - grey, 255 - grey, 25 - int(i * factor)))

		# Draw the text centered at (h_text_center, v_text_center) sized to have letters 5% of the image's height
		I1.multiline_text((h_text_center, v_text_center), poem, fill=(grey, grey, grey), anchor='ma',
						  font=ImageFont.truetype("arial.ttf", int(height * 0.03)))

		if PRODUCTION_RUN:
			# Save the edited image
			filepath = f"imgs/{item.split('.')[0]}/edited{count}.jpg"
			img.save(filepath)
			filepaths.append(filepath)
		else:
			img.show()
			input("Press enter to continue")
		count += 1

if PRODUCTION_RUN:
	# write filepaths to file so we can use them later
	with open("filepaths.txt", "w") as file:
		file.write("\n".join(filepaths))
