# open file read to string
f = "cloudy"
filename = f"{f}_in.txt"

with open(filename, "r") as file:
	data = file.read()

# for each line, delete the first 4 characters if they are "    "

lines = data.split("\n")
for i in range(len(lines)):
	if lines[i][:4] == "    ":
		lines[i] = lines[i][4:]

# join the lines back together
data = "\n".join(lines)

poems = data.split("Memorize Poem")

# enumerate thru poems
for i, poem in enumerate(poems):
	sections = poem.split("Full Text")
	if len(sections) == 1:
		sections = poem.split("\n\n")
	print(i)
	lines = sections[1]
	lines.strip()
	lines = lines.split("\n")
	for j in range(len(lines)):
		if lines[j][:4] == "    ":
			lines[j] = lines[j][4:]

	sections[1] = "\n".join(lines)
	poems[i] = "\n".join(sections)

out = "\n===\n".join(poems).replace("▼", "").replace("â–º", "")

while "\n\n" in out:
	out = out.replace("\n\n", "\n")

out = out.replace("\n \n", "\n")

# write to file
with open(f"{f}.txt", "w") as file:
	file.write(out)
