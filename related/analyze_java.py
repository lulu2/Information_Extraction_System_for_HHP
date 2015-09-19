#This is an simple program to analyze a lengthy java file as an alternative to javadoc.
#It basically works though not thoroughly.
from sys import argv

script, filename = argv
def collectionDetect(string):
	if string.find('<') != -1 and string.find('>') != -1:
		return True

def parseLine(line):
	temp = line.replace(", ", ",").strip()
	tempOutput = temp.split(' ')
	output=tempOutput[:]
	bufferElement = ''
	inArgument = False
	for element in output:
		position = tempOutput.index(element)
		argStart = element.find('(')
		argEnd = element.find(')')
		argEmpty = element.find('()')
		if argStart != -1 and argEmpty == -1:
			inArgument = True
			newElement = element[:argStart]
			bufferElement = ''.join([bufferElement,element[argStart:]])
			tempOutput.remove(element)
			if newElement != '':
				tempOutput.insert(position, newElement)
		elif argEnd != -1 and argEmpty == -1:
			bufferElement = ' '.join([bufferElement,element])
			tempOutput.remove(element)
			tempOutput.insert(position, bufferElement)
			bufferElement = ''
			inArgument = False
		elif inArgument:
			bufferElement = ' '.join([bufferElement,element])
			tempOutput.remove(element)
		elif argEmpty != -1:
			newElement = element[:argStart]
			tempOutput.insert(position, newElement)
			tempOutput.insert(position + 1, '()')
			tempOutput.remove(element)
	tempOutput_copy = tempOutput[:]
	candidateExist = False
	for element in tempOutput_copy:
		candidateBuffer = []
		if not collectionDetect(element):
			candidateExist = False
			candidateBuffer = []
		elif collectionDetect(element) and not candidateExist:
			candidateExist = True
			candidateBuffer = [element]
		elif collectionDetect(element) and candidateExist:
			candidateExist = False
			candidateBuffer.append(element)
			target = ' '.join(candidateBuffer)
			position = tempOutput.index(element)
			tempOutput.insert(position, target)
			tempOutput.remove(element)
			tempOutput.remove(candidateBuffer[0])
			candidateBuffer = []
	return tempOutput

def keywordClean(lineList, keywords):
	count = 0
	for keyword in keywords:
		if lineList.count(keyword) > 0:
			lineList.remove(keyword)
			count += 1
	return count

def keywordFilter(lineList):
	lineList_copy = lineList[:]
	keywordExist = keywordClean(lineList, ['{', '}', "public", "protected", "private", "final", "static", "abstract"])
	if keywordExist > 0:
		if lineList_copy.count('{') > 0:
			endPoint = lineList_copy.index('{')
			output = lineList_copy[:endPoint]
			keywordClean(output, ["public", "protected", "private", "final", "static", "abstract"])
			return output
		else:
			return lineList
	else:
		return []

def removeComments(line):
	if line.find('*') != -1 or line.find('//') != -1:
		return ''
	else:
		return line

def detectVariable(lineList):
	if lineList.count("new") > 0:
		return True
	else:
		return False

def argumentSythesis(dictionaryList):
	argumentList = []
	nameList = []
	outputList = dictionaryList[:]
	for dictionary in dictionaryList:
		name = dictionary['Name']
		argument = dictionary['Argument']
		if nameList.count(name) > 0:
			namePosition = nameList.index(name)
			methodPosition = dictionaryList.index(dictionary)
			argumentList[namePosition].append(argument)
			outputList[namePosition]['Argument'] = argumentList[namePosition]
			outputList.remove(dictionary)
		else:
			nameList.append(name)
			argumentList.append([argument])
	return outputList

# Read file into list
classFile = (open(filename)).read()
classLines = classFile.split('\n')
classLines = [line.strip() for line in classLines]
classLines = [removeComments(line) for line in classLines]
numBlank = classLines.count('')
for i in range(0,numBlank):
	classLines.remove('')
classLines = [line.strip(';') for line in classLines]

currentPosition = 0
#print classLines

# Get package name
packageLine = classLines[0].split(' ')
if packageLine[0] == "package":
	packageName = packageLine[1].split('.').pop()
	currentPosition += 1
else:
	print "Somthing is wrong in Get package name"


# Get import information
importStanford = []
importJava = []
importOthers = []

for line in classLines[currentPosition:]:
	importLine = line.split(' ')
	if importLine[0] == "import":
		currentPosition += 1
		importClass = importLine[1].split('.')
		if importClass[1] == "stanford":
			importStanford.append(".".join(importClass[3:]))
		elif importClass[0] == "java":
			importJava.append(".".join(importClass[1:]))
		else:
			importOthers.append(".".join(importClass[0:]))
	elif importLine[0] == '':
		currentPosition += 1
	else:
		break


# Get class general information
classInformation = {}
for line in classLines[currentPosition:]:
	currentPosition += 1 
	classLine = parseLine(line)
	if classLine[0] == "public":
		if classLine[1] == "abstract":
			classInformation["Abstract"] = "Y"
			classInformation["Type"] = "class"
			classInformation["Name"] = classLine[3]
			classInformation["Dependece type"] = classLine[4]
			classInformation["Dependence object"] = classLine[5]
		elif classLine[1] == "interface":
			classInformation["Abstract"] = "Y"
			classInformation["Type"] = "interface"
			classInformation["Name"] = classLine[2]
			classInformation["Dependece type"] = classLine[3]
			classInformation["Dependence object"] = classLine[4]
		elif classLine[1] == "class":
			classInformation["Abstract"] = "N"
			classInformation["Type"] = "class"
			classInformation["Name"] = classLine[2]
			classInformation["Dependece type"] = classLine[3]
			classInformation["Dependence object"] = classLine[4]
		else:
			currentPosition -= 1
			print "Somthing is wrong in Get class general information"

		break

# Get class variable and method information
variables = []
methods = []
constructors = []
inMethod = False
inConstructor = False
isMethodDeclaration = False
isConstructorDeclaration = False
structureDepth = 0

for line in classLines[currentPosition:]:
	parsedLine = parseLine(line)
	originLine = parsedLine[:]
	# Deceide wether it is constructor, variable, or method
	wordLength = len(keywordFilter(originLine))
	if not inMethod and not inConstructor:
		if wordLength == 3 and line.find('=') == -1:
			inMethod = True
			isMethodDeclaration = True
		elif wordLength == 2 and line.find('(') != -1 and parsedLine[0] != "for" and parsedLine[0] != "if" and line.find('=') == -1:
			inConstructor = True
			isConstructorDeclaration = True

	if not inMethod and not inConstructor:
		variableParse = {}
		if (parsedLine[0] == "public") or (parsedLine[0] == "protected") or (parsedLine[0] == "private"):
			if parsedLine[1] == "static":
				if parsedLine[2] != "final":
					variableParse["Access"] = parsedLine[0]
					variableParse["Type"] = parsedLine[2]
					variableParse["Name"] = parsedLine[3]
				else:	
					variableParse["Access"] = parsedLine[0]
					variableParse["Type"] = parsedLine[3]
					variableParse["Name"] = parsedLine[4]
			else:
				variableParse["Access"] = parsedLine[0]
				variableParse["Type"] = parsedLine[1]
				variableParse["Name"] = parsedLine[2]
			variables.append(variableParse)
		elif len(parsedLine) != 1:
			variableParse["Access"] = "None"
			variableParse["Type"] = parsedLine[0]
			variableParse["Name"] = parsedLine[1]
			variables.append(variableParse)	
	elif inConstructor:
		if line.find("{") != -1:
			structureDepth += 1
		if line.find("}") != -1:
			structureDepth -= 1

		if structureDepth == 0 and not isConstructorDeclaration:
			inConstructor = False
			isConstructorDeclaration = False

		if isConstructorDeclaration:
			constructorParse = {}
			if parsedLine[0] == "public":
				constructorParse["Access"] = parsedLine[0]
				constructorParse["Name"] = parsedLine[1]
				constructorParse["Argument"] = parsedLine[2]
			else:
				constructorParse["Access"] = "None"
				constructorParse["Name"] = parsedLine[0]
				constructorParse["Argument"] = parsedLine[1]			
			constructors.append(constructorParse)
			isConstructorDeclaration = False
	elif inMethod:
		if line.find("{") != -1:
			structureDepth += 1
		if line.find("}") != -1 or line.find("};") != -1:
			structureDepth -= 1

		if structureDepth == 0 and not isMethodDeclaration and parsedLine.count("abstract") == 0:
			inMethod = False

		if parsedLine.count("abstract") > 0:
			inMethod = False

		methodParse = {}
		if isMethodDeclaration and (parsedLine[0] == "public") or (parsedLine[0] == "protected") or (parsedLine[0] == "private"):
			if parsedLine[1] == "static":
				methodParse["Access"] = parsedLine[0]
				methodParse["Annotation"] = "static"
				methodParse["Return"] = parsedLine[2]
				methodParse["Name"] = parsedLine[3]
				methodParse["Argument"] = parsedLine[4]
			elif parsedLine[1] == "abstract":
				methodParse["Access"] = parsedLine[0]
				methodParse["Annotation"] = "abstract"
				methodParse["Return"] = parsedLine[2]
				methodParse["Name"] = parsedLine[3]
				methodParse["Argument"] = parsedLine[4]
			elif parsedLine[1] == "final":
				methodParse["Access"] = parsedLine[0]
				methodParse["Annotation"] = "final"
				methodParse["Return"] = parsedLine[2]
				methodParse["Name"] = parsedLine[3]
				methodParse["Argument"] = parsedLine[4]
			else:
				methodParse["Access"] = parsedLine[0]
				methodParse["Annotation"] = "None"
				methodParse["Return"] = parsedLine[1]
				methodParse["Name"] = parsedLine[2]
				methodParse["Argument"] = parsedLine[3]
			methods.append(methodParse)
		elif isMethodDeclaration:
			methodParse["Access"] = "None"
			methodParse["Annotation"] = "None"
			methodParse["Return"] = parsedLine[0]
			methodParse["Name"] = parsedLine[1]
			methodParse["Argument"] = parsedLine[2]
			methods.append(methodParse)
		isMethodDeclaration = False

#Sythesis of methods and constructors
methodList = argumentSythesis(methods)
constructorList = argumentSythesis(constructors)

print "CONSTRUCTOR IS"
print constructorList
print "PACKAGE NAME IS"
print packageName
print "IMPORTS FROM STANFORD ARE"
print importStanford
print "IMPORTS FROM JAVA ARE"
print importJava
print "CLASSINFORMATION ARE"
print classInformation
print "METHODS ARE"
print methodList
print "VARIABLES ARE"
print variables
print "METHODS NAME ARE"
for i in methodList:
	print i['Name']
'''
print "VARIABLE NAME ARE"
for i in variables:
	print i['Name']
'''



