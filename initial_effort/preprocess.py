from sys import argv
script, filename, loadname = argv

transformVocabulary = ['also', 'in']
dateVocabulary =[]

def parseBracket(line):
	line.replace('( ', '(')
	line.replace(' )', ')')
	dates = line.split(' ')
	output = dates[:]
	bufferElement = ''
	inArgument = False
	for element in output:
		position = dates.index(element)
		argStart = element.find('(')
		argEnd = element.find(')')
		argEmpty = element.find('()')
		if argStart != -1 and argEmpty == -1:
			inArgument = True
			newElement = element[:argStart]
			bufferElement = ''.join([bufferElement,element[argStart:]])
			dates.remove(element)
			if newElement != '':
				dates.insert(position, newElement)
		elif argEnd != -1 and argEmpty == -1:
			bufferElement = ' '.join([bufferElement,element])
			dates.remove(element)
			dates.insert(position, bufferElement)
			bufferElement = ''
			inArgument = False
		elif inArgument:
			bufferElement = ' '.join([bufferElement,element])
			dates.remove(element)
		elif argEmpty != -1:
			newElement = element[:argStart]
			dates.insert(position, newElement)
			dates.insert(position + 1, '()')
			dates.remove(element)
	return dates

def parseNames(tokens):
	if tokens.count('') != 0:
		tokens.remove('')
	tokensCopy = tokens[:]
	tokenBuffer = ''
	insertPosition = 0
	inToken = False
	for element in tokensCopy:
		tokenIndex = tokens.index(element)
		if element[0].isupper():
			if inToken == True:
				tokenBuffer = ' '.join([tokenBuffer,element])
			else:
				tokenBuffer = ''.join([tokenBuffer,element])
			inToken = True
			tokens.remove(element)
			insertPosition = tokenIndex
		elif inToken and element[0].islower():
			inToken = False
			tokens.insert(insertPosition, tokenBuffer)
			tokenBuffer = ''
	if tokenBuffer !='':
		tokens.append(tokenBuffer)
	return tokens

def transform(tokens):
	if tokens.count('') != 0:
		tokens.remove('')
	tokensCopy = tokens[:]
	tokenBuffer = []
	inTransform = False
	insertPosition = 0
	insertBufffer =[]
	for element in tokensCopy:
		tokenIndex = tokens.index(element)
		if element[0].isupper():
			tokenBuffer.insert(0, element)
			inTransform = True
		elif inTransform and element[0] == '(':
			content = element.strip('(').strip(')')
			wordList = content.split(' ')
			key = wordList[0]
			addedSentence = ''
			if transformVocabulary.count(key) > 0:
				addedSentence = ' is '.join([tokenBuffer[0],content])
				insertBufffer.insert(0,addedSentence)
				tokens.remove(element)
			elif wordList.count(u'\u2013'.encode('utf-8')) > 0:
				division = wordList.index(u'\u2013'.encode('utf-8'))
				birthDate = ' '.join([wordList[division - 2], wordList[division - 1]])
				deathDate = ' '.join([wordList[division + 1], wordList[division + 2]])
				addedSentence_1 = ' was born in '.join([tokenBuffer[0], birthDate])
				addedSentence_2 = ' was born in '.join([tokenBuffer[0], deathDate])
				addedSentence = '. '.join([addedSentence_1, addedSentence_2])
				insertBufffer.insert(0,addedSentence)
				tokens.remove(element)
	for i in insertBufffer:
		tokens.append('.')
		tokens.append(i)
	tokens.append('.')
	return tokens

### Following is the main part
readFile = (open(filename)).read()
paras = readFile.split('\n')
contentBuffer = []
for para in paras:
	lines = para.split('.')
	lines.remove('')
	lines2 = [sentence.strip() for sentence in lines]
	tokenList = [parseBracket(line) for line in lines2]
	chunkList = [parseNames(token) for token in tokenList]
	output = [transform(chunk) for chunk in chunkList]
	contentBuffer.append(output)

### Write File
loadFile = open(loadname, 'w')
for i in contentBuffer:
	for j in i:
		counter = len(j)
		for k in range(0, counter - 1):
			loadFile.write(j[k])
			if j[k + 1] !='.':
				loadFile.write(' ')
		loadFile.write(j[counter - 1])
		if j[counter - 1] != '.':
			loadFile.write('.')
			loadFile.write(' ')
		else:
			loadFile.write(' ')
	loadFile.write("\n")
loadFile.close()

#classLines = [clearReading(line) for line in classLines]
#tokenList = [parseBracket(line) for line in classLines]
#kk = [parseNames(token) for token in tokenList]
#print kk