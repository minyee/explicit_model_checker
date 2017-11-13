import kripke_structure
import sys
import file
import io
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP

def parseKripFile(filename):
	kripFile = Open(filename, 'r') # open file read only
	line = kripFile.readline()
	numStates = int(line)
	states = {}
	currId = 0
	while line:
		tokens = tokenize(line, ": {,}")
		isAp = True
		apDictForState = {}
		apSymbol = "r"
		apValue = True
		for toknum, tokval, _, _, _ in tokens:
			if toknum == 0:
				currId = int(tokval)
			else:
				if isAp:
					apSymbol = tokval
				else:
					if int(tokval) == 1:
						apValue = True
					else:
						apValue = False
					apDictForState.insert(apSymbol, apValue)
			isAp = not isAp
		states = State(currId, adjacencyList, apDictForState)

		line = kripFile.readline()

		State(id)
		#prepare for next iteration
		line = kripFile.readline()

	kripFile.close()
	ks = KripkeStructure()
	return ks

def satAP(KripkeSet,apDict):
	outputSet = [0]
	i = 0
	for state in KripkeSet:
		if state.satisfyAP()
			outputSet.insert(i, state)
			i += 1
	return outputSet

def satEX(APdictArg, kripkeStructure):
	firstSet = [0]
	i = 0
	for state in kripkeStructure:
		if state.satisfyAP(APdictArg):
			firstSet.insert(i, state)
			i += 1
	secondSet = [0]
	i = 0
	for state in kripkeStructure:
		for neighborState in firstSet:
			if state.isNeighbor(neighborState):
				secondSet.insert(i, state)
				i += 1
	return secondSet

def satisfy(KripkeSet, ctlStructure) :
	# negligible case
	if ctlStructure.getOp() == None:
		return None
	elif ctlStructure.getOp() == TRUE:
		return KripkeSet
	elif ctlStructure.getOp() == FALSE:
		return None
	elif ctlStructure.getOp() == AP:
		return satAP(KripkeSet, ctlStructure.getAPdict())
	elif ctlStructure.getOp() == NOTAP:
		#call
	elif ctlStructure.getOp() == OR:
		#call
	elif ctlStructure.getOp() == EX:
		#call
	elif ctlStructure.getOp() == EU:
		#call
	else:
		#finally the case has to be EG
		#call
def modelCheckerMain(file1, file2):
	kripkeStruct = parseKripFile(file1)
