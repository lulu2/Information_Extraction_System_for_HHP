#This is a simple information extraction implementation based on dependency graph analysis.
#Not thorough but suggests that this method works. It is based on dependency graph analysis
#result of StanfordNLP. This script works on the output file of dependency graph analysis.
import math
from sys import argv
script, filename = argv

extractions = []
compoundList = []
nsubjList = []
conjList = []
apposList = []
advmodList = []
depList = []
nummodList = []
copList = []
detList = []
amodList = []

def removeDuplicates(values):
    output = []
    pool = []
    for value in values:
        if pool.count(value) == 0:
            output.append(value)
            pool.append(value)
    return output

def mergeList(A, p, q, r):
	B = []
	n_1 = q - p + 1
	n_2 = r - q
	L = []
	R = []
	for i in range(0, n_1):
		L.append(A[p + i])
	for j in range(0, n_2 ):
		R.append(A[q + j + 1])
	L.append(float('inf'))
	R.append(float('inf'))
	i = 0
	j = 0
	for k in range(p, r + 1):
		if L[i][1] < R[j][1]:
			B.append(L[i])
			i = i + 1
		elif L[i][1] > R[j][1]:
			B.append(R[j])
			j = j + 1
		elif L[i] != float('inf'):
			B.append(R[i])
			i = i + 1
			j = j + 1
	return B

def getConj(lists):
	List =[]
	for i in lists:
		output = ""
		pairList = []
		for j in i:
			if output == "":
				output = j[0]
			else:				
				output = output + " and " + j[0]
			pairList.append(j)
		List.append([output,pairList])
	return List

def addByTwo(listInput):
	output = []
	iterations = len(listInput)/2
	for i in range(0,iterations):
		output.append([listInput[2*i],listInput[2*i + 1]])
	return output

def partialList(A,B):
	for i in A:
		if (A[0] == B[0] and A[1]!= B[1]) or A[1] == B[0] or A[0] == B[1] or (A[1] == B[1] and A[0]!= B[0]):
			return True
		else:
			return False

def getCoverage(A,B):
	for i in A:
		if (A[0] == B[0] and A[1]!= B[1]) or A[0] == B[1]:
			return A[0][0]
		elif A[1] == B[0] or (A[1] == B[1] and A[0]!= B[0]):
			return A[1][0]

def getKeyword(string):
	if string.find(':') == -1:
		endCharacter = string.find('(')
	else:
		endCharacter = string.find(':')
	return string[0: endCharacter]

def getComponent(string):
	startCharacter = string.find('(')
	component = string[startCharacter + 1: -1]
	componentList = component.split(', ')
	output = []
	candidate = [element.split('-') for element in componentList]
	for tuple in candidate:
		output.append([tuple[0], tuple[1]])
	if string.find(':') != -1:
		output.append(string[string.find(':') + 1:string.find('(')])
	return output

def sortByKey(componentsList, keysList):
	if int(keysList[1]) < int(keysList[0]):
		position_0 = componentsList[0]
		position_1 = componentsList[1]
		componentsList[0] = position_1
		componentsList[1] = position_0
	return componentsList

def compoundInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " " + output[1])

def nsubjInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " is " + output[1])

def conjInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " " + componentList[2] + " " + output[1])

def apposInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " is " + output[1])

def advmodInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " " + output[1])

def depInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " " + output[1])

def nummodInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " " + output[1])

def copInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " " + output[1])

def detInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " " + output[1])

def amodInterpreter(componentList):
	keys = [componentList[0][1], componentList[1][1]]
	components = [componentList[0][0], componentList[1][0]]
	output = sortByKey(components, keys)
	return (output[0] + " " + output[1])

readFile = (open(filename)).read()
denpendencies = readFile.split('\n')
# Following is to preprocess the dependencies
for denpendency in denpendencies:
	keyword = getKeyword(denpendency)
	component = getComponent(denpendency)
	if keyword == 'compound':
		compoundElement = compoundInterpreter(component)
		compoundList.append([compoundElement, component])
	elif keyword == 'nsubj':
		nsubjElement = nsubjInterpreter(component)
		nsubjList.append([nsubjElement, component])
	elif keyword == 'conj':
		conjElement = conjInterpreter(component)
		conjList.append([conjElement, component])
	elif keyword == 'appos':
		apposElement = apposInterpreter(component)
		apposList.append([apposElement, component])
	elif keyword == 'advmod':
		advmodElement = advmodInterpreter(component)
		advmodList.append([advmodElement, component])
	elif keyword == 'dep':
		depElement = depInterpreter(component)
		depList.append([depElement, component])
	elif keyword == 'nummod':
		nummodElement = nummodInterpreter(component)
		nummodList.append([nummodElement, component])
	elif keyword == 'cop':
		copElement = copInterpreter(component)
		copList.append([copElement, component])
	elif keyword == 'det':
		detElement = detInterpreter(component)
		detList.append([detElement, component])
	elif keyword == 'amod':
		amodElement = amodInterpreter(component)
		amodList.append([amodElement, component])
#Following is to deal with dependencies

#Deal with conj
conjFinal = []
conjCandidates = []
for conj in conjList:
	conjCandidates.append([conj[1][0],conj[1][1]])
conjCandidatesLength = len(conjCandidates)
for i in range(0,conjCandidatesLength):
	for j in range(i+1,conjCandidatesLength):
		if partialList(conjCandidates[i], conjCandidates[j]):
			item = removeDuplicates(conjCandidates[i] + conjCandidates[j])
			conjFinal.append(item)
conjList = getConj(conjFinal)


#Deal with nsubj
for i in nsubjList:
	temp = []
	for j in compoundList:
		if partialList(j[1], i[1]):
			part = getCoverage(j[1],i[1])
			k = i[0].replace(part,j[0])
			i[0] = k
	for j in conjList:
		if partialList(j[1], i[1]):
			part = getCoverage(j[1],i[1])
			k = i[0].replace(part,j[0])
			i[0] = k
output = nsubjList[0][0].split(' is ')
output.insert(1,'is')
print output

