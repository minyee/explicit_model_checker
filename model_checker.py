import kripke_structure
import sys
#import file
import io
from ctl_ops import *
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP


def findORWithinBound(charList, start, end):
	i = 0
	while start + i <= end:
		if charList[start + i] == "|":
			return (start + i)
	return (-10)

# NOTE: returns a offset greater than end if the closing parenthesis is not found
def findCloseParenIndex(charList, offset, end):
	assert(offset >= 0)
	foundAnotherOpenParen = 0
	iterate = True
	while iterate:
		offset += 1
		if offset > end:
			#SHIT WE HAVE A PROBLEM
			return -22
		assert(foundAnotherOpenParen >= 0)
		if charList[offset] == "(":
			foundAnotherOpenParen += 1
		elif charList[offset] == ")":
			if foundAnotherOpenParen == 0:
				iterate = False
				break
			else:
				foundAnotherOpenParen -= 1

	return offset


#Note: this function will only work correctly when there is a correct nesting structure
def parseCTLRecursive(charList, start, end):
	#	ctlStructure = CTLNestedStructure()
	#Base case for when the argument is an empty string
	string = ""
	for i in range(start, end+1, 1):
		string += charList[i]

	print string

	assert(start <= end)
	# Case 1: Just an AP (Base Case) or Trivial Cases TRUE and FALSE
	if start == end:
		ctlStruct = None
		if charList[start] == "T":
			ctlStruct = CTLNestedStructure(CTLOperators.TRUE, None)
		elif charList[start] == "F":
			ctlStruct = CTLNestedStructure(CTLOperators.FALSE, None)
		else:
			assert(charList[start].islower())
			ctlStruct = CTLNestedStructure(CTLOperators.AP, charList[start])
			print charList[start]
		return ctlStruct
	
	# Case 2: find account for the OR, we restrict the structure to look like: (exp) | (exp)
	elif charList[start] == "(": 
		orIndex = findCloseParenIndex(charList, start, end) + 1
		assert(orIndex >= 0 and orIndex > start and orIndex < end)
		leftCTL = parseCTLRecursive(charList, start + 1, orIndex - 2)
		assert(charList[orIndex + 1] == "(" and charList[end] == ")")
		rightCTL = parseCTLRecursive(charList, orIndex + 2, end - 1)
		ctlStruct = CTLNestedStructure(CTLOperators.OR, None)
		ctlStruct.addNestedOp(leftCTL, rightCTL, None)
		return ctlStruct
	# Case 3: first for the cases for E, there are three distinct possibilities
	elif charList[start] == "E": 
		# EX
		if charList[start + 1] == "X":
			assert(charList[start + 2] == "(")
			offset = start + 2
			closedParenIndex = findCloseParenIndex(charList, offset, end)
			assert(closedParenIndex == end)
			ctlStructure = CTLNestedStructure(CTLOperators.EX, None)
			nestedStruct = parseCTLRecursive(charList, start + 3, closedParenIndex - 1)
			ctlStructure.addNestedOp(nestedStruct, None, None)
			return ctlStructure
		
		#EG
		elif charList[start + 1] == "G":
			assert(charList[start + 2] == "(")
			offset = start + 2
			closedParenIndex = findCloseParenIndex(charList, offset, end)
			assert(closedParenIndex == end)
			ctlStructure = CTLNestedStructure(CTLOperators.EG, None)
			nestedStruct = parseCTLRecursive(charList, start + 3, closedParenIndex - 1)
			ctlStructure.addNestedOp(nestedStruct, None, None)
			return ctlStructure
		
		#E(exp1)U(exp2)
		else:
			assert(charList[start + 1] == "(")
			offset = start + 1
			closedParenIndex = findCloseParenIndex(charList, offset, end)
			assert(closedParenIndex >= 0 and closedParenIndex <= end)
			assert(charList[closedParenIndex + 1] == "U")
			assert(charList[end] == ")")
			left = parseCTLRecursive(charList, offset + 1, closedParenIndex - 1)
			right = parseCTLRecursive(charList, closedParenIndex + 3, end - 1)
			ctlStructure = CTLNestedStructure(CTLOperators.EU, None)
			ctlStructure.addNestedOp(left, right, None)
			return ctlStructure

	#Case 4: the NOT case
	elif charList[start] == "~": # The case for ~(exp)
		assert(charList[start + 1] == "(")
		assert(charList[end] == ")")
		nestedStruct = parseCTLRecursive(charList, start + 1, end - 1)
		ctlStructure = CTLNestedStructure(CTLOperators.NOT, None)
		ctlStructure.addNestedOp(nestedStruct, None, None)
		return ctlStructure

	return None

def parseCTLString(ctlFormula):
	charList = list(ctlFormula)
	return parseCTLRecursive(charList, 0, len(charList) - 1)


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
	outputSet = []
	i = 0
	#print len(KripkeSet)
	for state in KripkeSet.getGraphNodeList():
		if state.satisfyAP(apDict):
			outputSet.append(state)
			i += 1

	return outputSet

def satNOTAP(KripkeSet, apDict):
	apDictNew = {}
	for key, val in apDict:
		val = not val
		apDictNew.insert(key, val)
	return satAP(KripkeSet, apDictNew)

def satEX(kripkeStructure, KripkeSet, ctlStructure):
	ctlOp1, _ = ctlStructure.getNestedOp() 
	firstSet = satisfy(kripkeStructure, KripkeSet, ctlOp1)
	#APdictArg = ctlStructure.getAPdict()
	secondSet = []
	reversedGraph = kripkeStructure.getReversedGraph()

	for state in firstSet:
		currID = state.getId()
		reversedAdjacencyList = reversedGraph[currID].getAdjacencyList()
		for neighborState in reversedGraph:
			if neighborState.getId() not in secondSet:
				secondSet.append(neighborState.getId())

	thirdSet = []
	for state in kripkeStructure.getGraphNodeList():
		if state.getId() in secondSet:
			thirdSet.append(state)

	return thirdSet

# TODO: Check correctness of implementation
def satEU(KripkeStructure, KripkeSet, ctlStructure):
	ctlOp1, ctlOp2 = ctlStructure.getNestedOp()
	Q = satisfy(KripkeSet, ctlStructure.ctlOp2)
	iterate = True
	while iterate:
		iterate = False
		for state in Q:
			reversedGraphNeighborList = state.getReversedGraphNeighborList(state.getId())
			newQ = satisfy(KripkeStructure,reversedGraphNeighborList, ctlOp1)
			if len(newQ) > 0:
				Q = unionSets(newQ, Q)
				iterate = True	
	return Q

def satEG(KripkeStructure, KripkeSet, ctlStructure):
	ctlop1, ctlop2 = ctlStructure.getNestedOp
	Q = satisfy(KripkeStructure, KripkeSet, ctlop1)
	QID = [0] * len(Q)
	#i = 0
	subGraphList = {}
	for state in Q:
		subGraphList.insert(state.getId(), Node(state.getId()))

	#Generate subgraph to find SCC
	subgraph = Graph(subGraphList)
	for state in Q:
		node = KripkeStructure.getNode(state.getId())
		for neighbor in node.getAdjacencyList():
			if neighbor.getId in subGraphList.keys():
				state.addNeighbor(subGraphList[neighbor.getId])

	#Done generating subgraph
	reversedSubGraph = subgraph.getReversedGraph()
	sccs = subgraph.findSCC()
	#Note: sccs is a 
	finalNodes = {}
	for cycles in sccs:
		for node in cycles:
			if node.getId() not in finalNodes.keys():
				finalNodes.insert(node.getId(), node)
			for srcNode in reversedSubGraph.getNode(node.getId()).getAdjacencyList:
				if srcNode.getId() not in finalNodes.keys():
					finalNodes.insert(srcNode.getId(), srcNode)
	finalStates = []
	for key, val in finalNodes:
		i = 0
		for state in KripkeSet:
			if state.getId() == key:
				finalStates.append(KripkeSet[i])
				break
			else:
				i+=1

	return finalStates

# Finds the union of two sets, S1, and S2
# Note: S1, S2 are given as lists
def unionSets(S1, S2):
	union = [0]
	
	if S1 == None:
		return S2
	if S2 == None:
		return S1

	size1 = len(S1)
	size2 = len(S2)
	totalSize = size1 + size2
	for i in range(size1):
		union.insert(i, S1[i])
	for i in range(size2):
		if S2[i] not in union:
			union.insert(i + size1, S2[i])
	return union

# TODO: Given a ctl formula string, create a CTLstructure data type which
# is recursive so that the CTLStructure and satisfy method defined below can work
def parseCTLFormula(formulaString):

	return 

# Main recursive routine to check if a Kripke Structure
# satisfies a CTL statement, which is recursive and is fed as
# the argument ctlStructure. The KripkeStructure argument is the
# the whole Kripke structure, while KripkeSet is the subset of states
# in KripkeSet that satisfies some previous conditions
def satisfy(KripkeStructure, KripkeSet, ctlStructure) :
	# negligible case
	if ctlStructure.getOp() == None:
		return None
	elif ctlStructure.getOp() == CTLOperators.TRUE:
		return KripkeSet
	elif ctlStructure.getOp() == CTLOperators.FALSE:
		return None
	elif ctlStructure.getOp() == CTLOperators.AP:
		return satAP(KripkeSet, ctlStructure.getLabel())
	elif ctlStructure.getOp() == CTLOperators.NOT:
		return satNOTAP(KripkeSet, ctlStructure.getLabel())
	elif ctlStructure.getOp() == CTLOperators.OR:
		nestedOp1, nestedOp2 = ctlStructure.getNestedOp()
		S1 = satisfy(KripkeStructure, KripkeSet, nestedOp1)
		S2 = satisfy(KripkeStructure, KripkeSet, nestedOp2)
		return union(S1,S2)
	elif ctlStructure.getOp() == CTLOperators.EX:
		#nestedOp1, nestedOp2 = ctlStructure.getNestedOp()
 		return satEX(KripkeStructure, KripkeSet, ctlStructure) ## CHECK THIS, THIS IS WRONG. EX needs to be recursive
	elif ctlStructure.getOp() == CTLOperators.EU:
		return satEU(KripkeStructure, KripkeSet, ctlStructure)
	else:
		return satEG(KripkeStructure, KripkeSet, ctlStructure)

#def modelCheckerMain(file1, file2):
#	kripkeStruct = parseKripFile(file1)
