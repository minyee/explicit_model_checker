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

def satNOTAP(KripkeSet, apDict):
	apDictNew = {}
	for key, val in apDict:
		val = not val
		apDictNew.insert(key, !val)
	return satAP(KripkeSet, apDict)

# TODO: Needs correction for recursive nested CTL operations
def satEX(kripkeStructure, ctlStructure):
	firstSet = [0]
	APdictArg = ctlStructure.getAPdict()
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
	
	size1 = len(S1)
	size2 = len(S2)
	totalSize = size1 + size2
	for i in range(size1):
		union.insert(i, S1[i])
	for i in range(size2):
		if S2[i] not in union:
			union.insert(i + size1, S2[i])
	return union

# Main recursive routine to check if a Kripke Structure
# satisfies a CTL statement, which is recursive and is fed as
# the argument ctlStructure. The KripkeStructure argument is the
# the whole Kripke structure, while KripkeSet is the subset of states
# in KripkeSet that satisfies some previous conditions
def satisfy(KripkeStructure, KripkeSet, ctlStructure) :
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
		return satNOTAP(KripkeSet, ctlStructure.getAPdict())
	elif ctlStructure.getOp() == OR:
		nestedOp1, nestedOp2 = ctlStructure.getNestedOp()
		S1 = satisfy(KripkeStructure, KripkeSet, nestedOp1)
		S2 = satisfy(KripkeStructure, KripkeSet, nestedOp2)
		return union(S1,S2)
	elif ctlStructure.getOp() == EX:
 		return satEX(KripkeStructure, KripkeSet, ctlStructure) ## CHECK THIS, THIS IS WRONG. EX needs to be recursive
	elif ctlStructure.getOp() == EU:
		return satEU(KripkeStructure, KripkeSet, ctlStructure)
	else:
		return satEG(KripkeStructure, KripkeSet, ctlStructure)

def modelCheckerMain(file1, file2):
	kripkeStruct = parseKripFile(file1)
