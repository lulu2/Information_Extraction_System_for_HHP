from sys import argv
script, filename, loadname = argv

PRPList = ["He", "he", "She", "she", "His", "his", "Her", "her"]
outputFile = (open(filename)).read()
outputLines = outputFile.split('\n')
loadLines = []
PRPPointer = ""
sentenceCounter = 0

for line in outputLines:
	if not line == '':
		if not line[0].isdigit():
			sentenceCounter += 1
			loadLine = ["-----", ': '.join(["Line Number", str(sentenceCounter)]),"-----"]
			loadLines.append(loadLine)
		else:
			confidenceRate = float(line[0:5])
			if confidenceRate > 0.53:
				content = line[8:-1]
				loadLine = content.split('; ')
				subject = loadLine[0]
				if PRPList.count(subject) == 0:
					PRPPointer = subject
				elif PRPList.index(subject) < 4:
					loadLine[0] = PRPPointer
				else:
					loadLine[0] = "'".join([PRPPointer, "s"])
				loadLines.append(loadLine)

loadFile = open(loadname, 'w')
for i in loadLines:
	loadFile.write(i[0])
	loadFile.write("\n")
	loadFile.write(i[1])
	loadFile.write("\n")
	loadFile.write(i[2])
	loadFile.write("\n")
loadFile.close()