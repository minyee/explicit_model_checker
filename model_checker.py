import kripke_structure
import sys
#import file
import io
from ctl_ops import *
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from collections import deque
from vhdlParser import *
from recursiveNS import *

def bfs(kripkeStructure, srcNode, satisfyingStates):
	currNode = srcNode
	nodeQueue = []
	size = len(graphNodeList)
	visited = [False] * size
	nodeQueue.append(srcNode)
	visited[currNode.getId()] = True
	while len(nodeQueue) > 0:
		currNode = nodeQueue.deque()
		visited[currNode.getId()] = True
		for neighbor in currNode.getAdjacencyList():
			#only consider nodes that are in the graphNodeList
			if neighbor in satisfyingStates:
				if not visited[neighbor.getId()]:
					nodeQueue.append(neighbor)
	return

def findAXCounterExample(kripkeStructure,kripkeSet,initialState):
    '''
    Returns the first 1-step path from initial state that violates property.
    This is a comprehensive counterexample for AX
    '''
    for neighbor in initialState.getAdjacencyList():
        path = [initialState.getId()]
        if neighbor not in kripkeSet:
            path.append(neighbor.getId())
            return path

def findEXCounterExample(kripkeStructure,kripkeSet,initialState):
    '''
    Returns all 1-step paths from initial state. This is a comprehensive counterexample
    for EX
    '''
    paths = []
    for neighbor in initialState.getAdjacencyList():
        path = [initialState.getId()]
        path.append(neighbor.getId())
        paths.append(path)
    return paths

def findAllAGCounterExamples(kripkeStructure,kripkeSet,initialState,stateFound):
	'''
	finds all of them by changing a deepcopy of the kripke structure.
	stateFound is the last state found. If first call then set to None
	'''
	k_struct = copy.deepcopy(kripkeStructure)
	k_set = []
	for state in k_struct.graphNodeList:
		for node in kripkeSet:
			if node.id == state.id:
				k_set.append(state)
				break
	pathLists = []
	originalLength = len(k_set)
	for state in k_struct.graphNodeList:
		for i in range(len(state.getAdjacencyList())):
			path = findAGCounterExample(k_struct,k_set,k_struct.graphNodeList[0])
			while path:
				if path not in pathLists and path:
					pathLists.append(path)
				k_set.append(idToNode(path[len(path)-1],k_struct))
				path = findAGCounterExample(k_struct,k_set,k_struct.graphNodeList[0])
			for i in range(len(k_set) - originalLength):
				k_set.pop()
			rotateAdjacencyList(state)

	return pathLists

def findAGCounterExample(kripkeStructure,kripkeSet,initialState):
    '''
    modified dfs for AG conterexample generation
    '''
    nodeStack = []
    nodeStackList = []
    nodeStack.append(initialState)
    size = len(kripkeStructure.graphNodeList)
    visitedList = [False] * size

    while nodeStack:
        proceed = True
        currNode = nodeStack[len(nodeStack)-1]
        if currNode in kripkeSet:
            visitedList[currNode.id] = True
            if currNode.getAdjacencyList():
                for nextNode in currNode.getAdjacencyList():
                    if (visitedList[nextNode.id] == False) and (proceed == True):
                        nodeStack.append(nextNode)
                        proceed = False
                if proceed == True:
                    nodeStack.pop()
            else:
                nodeStack.pop()
        else:
            break

    return returnNodeStackIdList(nodeStack)

def findAFCounterExample(kripkeStructure,kripkeSet,initialState):
	'''
	just uses find AUCounterexample. AFp = A((TRUE)Up)
	'''
	return findAUCounterExample(kripkeStructure,kripkeStructure.graphNodeList,kripkeSet,initialState)

def findAUCounterExample(kripkeStructure,kripkeSet1,kripkeSet2,initialState):
	'''
	modified dfs for AU conterexample generation.
	A(KS1 U KS2)
	Runs DFS until it hits a !KS1 before KS2 OR until it hits an SCC state of KS1
	NEED TO ADD SCC TO COUNTEREXAMPLE! Technically what I have now is still correct.
	'''
	nodeStack = []
	nodeStackList = []
	nodeStack.append(initialState)
	size = len(kripkeStructure.graphNodeList)
	visitedList = [False] * size
	SCC_list,SCC_Set = returnSCCSet(kripkeStructure,kripkeSet1)
	#print SCC_list

	while nodeStack:
		proceed = True
		currNode = nodeStack[len(nodeStack)-1]

		if ((currNode in kripkeSet1) or (currNode in kripkeSet2)) and (currNode not in SCC_Set):
			visitedList[currNode.id] = True
			if currNode.getAdjacencyList():
				for nextNode in currNode.getAdjacencyList():
					if (visitedList[nextNode.id] == False) and (proceed == True):
						nodeStack.append(nextNode)
						proceed = False
				if proceed == True:
					nodeStack.pop()
			else:
				nodeStack.pop()
		else:
			if currNode in SCC_Set:
				for SCC in SCC_list:
					if currNode.id in SCC:
						print 'Smallest SCC: ' + str(SCC)
						break
			break

	return returnNodeStackIdList(nodeStack)

def findEUCounterExample(kripkeStructure,kripkeSet1,kripkeSet2,initialState):
	'''
	1. Checks to see if KS2 is empty. If so, CE is knowledge that it is empty
	2. Checks to see if initialState is in KS1. If not, CE is initial state
	3. checks to see if there exists a path from initial state to any KS2 states
	if so, CE is list of all paths to KS2 states and all states not in KS1 included in paths
	4. If none of these conditions are met then CE is knowledge KS2 is unreachable from initial state
	'''
	nodeStack = [initialState]
	CE = None

	if not kripkeSet2:
		CE = 'No states in KS2'
	elif initialState not in kripkeSet1:
		CE = returnNodeStackIdList(nodeStack)
	elif initialState in satEU(kripkeStructure,kripkeStructure.graphNodeList,kripkeSet2):
		complementKS2 = satNOT(kripkeStructure,kripkeSet2)
		print 'Violating States in Paths: ' + str(returnNodeStackIdList(kripkeSet2))
		CE = findAllAGCounterExamples(kripkeStructure,complementKS2,kripkeStructure.graphNodeList[0],None)
	else:
		CE = "KS2 unreachable from initial state"
	return CE

def findEFCounterExample(kripkeStructure,kripkeSet,initialState):
	'''
	just uses find EUCounterexample. AFp = A((TRUE)Up)
	'''
	return findEUCounterExample(kripkeStructure,kripkeStructure.graphNodeList,kripkeSet,initialState)

def satAP(KripkeSet,ApName):
    '''
    Returns set of states where AP is true
    '''
    returnSet = []
    #print len(KripkeSet)
    for state in KripkeSet.getGraphNodeList():
        if state.satisfyAP(ApName):
            returnSet.append(state)

    return returnSet

def satNOT(KripkeStructure,KripkeSet):
    '''
    Returns the set of states in kripke structure that aren't the states in
    kripke set
    '''
    returnSet = []
    for node in KripkeStructure.graphNodeList:
        if node not in KripkeSet:
            returnSet.append(node)
    return returnSet

def satEX(kripkeStructure, KripkeSet):
    '''
    returns set of states in kripkeStructure that have transitions to the states
    in the KripkeSet
	'''
    returnSet = []
    for state in KripkeSet:
		currID = state.getId()
		for pointingState in state.incomingEdges:
			if pointingState not in returnSet:
				returnSet.append(pointingState)
    return returnSet

def satEU(KripkeStructure, KripkeSet1, KripkeSet2):
	'''
	Returns set of states that satisfy E( KS1 U KS2 )
	iterative
	start with KS2 states
	find states in KS1 that point directly to KS2
	find states that point directly to these states
	iterate until set of states returned is empty
	'''
	returnSet = copy.copy(KripkeSet2)

	lastSet = copy.copy(KripkeSet2)
	while lastSet:
		currentSet = []
		for node in lastSet:
			for pointingState in node.incomingEdges:
				if (pointingState in KripkeSet1) and (pointingState not in returnSet):
					currentSet.append(pointingState)
					returnSet.append(pointingState)
		lastSet = currentSet

	return returnSet

def returnSCCSet(KripkeStructure, KripkeSet):
	'''
	Modified DFS. Finds all SCCs and all states with paths through KripkeSet to SCCs
	'''
	SCC_IdList = []
	returnStates = []
	SCC_nodeList = []
	size = len(KripkeStructure.graphNodeList)
	for initialState in KripkeSet:
		startState = initialState
		visitedList = [False] * size
		nodeStack = []
		nodeStackList = []
		nodeStack.append(initialState)

		while nodeStack:
			proceed = True
			currNode = nodeStack[len(nodeStack)-1]

			visitedList[currNode.id] = True

			if startState in currNode.getAdjacencyList():
				sortedStacks = []
				newStack1 = sorted(returnNodeStackIdList(nodeStack))
				for stack in SCC_IdList:
					sortedStacks.append(sorted(stack[:len(stack)-1]))
				if newStack1 not in sortedStacks:
					nodeStack.append(startState)
					SCC_IdList.append(returnNodeStackIdList(nodeStack))
					for node in nodeStack:
						if node not in returnStates:
							returnStates.append(node)
					nodeStack.pop()

			if currNode.getAdjacencyList():
				for nextNode in currNode.getAdjacencyList():
					#if nextNode == startState and (doneList[nextNode.id] == False) and (proceed == True):
					if (visitedList[nextNode.id] == False) and (nextNode in KripkeSet) and (proceed == True):
						nodeStack.append(nextNode)
						proceed = False
				if proceed == True:
					nodeStack.pop()
			else:
				nodeStack.pop()
	#print SCC_IdList
	#print returnNodeStackIdList(returnStates)
	return SCC_IdList, returnStates

def satEG(KripkeStructure, KripkeSet):
	'''
	Modified DFS. Finds all SCCs and all states with paths through KripkeSet to SCCs
	'''
	SCC_IdList, returnStates = returnSCCSet(KripkeStructure,KripkeSet)
	#print SCC_IdList
	returnStates = satEU(KripkeStructure, KripkeSet, returnStates)
	#print returnNodeStackIdList(returnStates)
	return returnStates

def satOR(S1, S2):
    '''
    Finds the union of two sets, S1, and S2
    '''
    union = []
    for node in S1:
        union.append(node)
    for node in S2:
        if node not in union:
            union.append(node)
    return union

def idToNode(nodeId,kripkeStructure):
	'''
	just returns the node corresponding to the id. Don't want to assume that
	you can just index the graphnode list
	'''
	for node in kripkeStructure.graphNodeList:
		if node.id == nodeId:
			return node
	return None

def returnNodeStackIdList(nodeStack):
	'''
	prints node stack
	'''
	nodeStackList = []
	#turn nodestack into id list
	for node in nodeStack:
		nodeStackList.append(node.id)
	return nodeStackList

def rotateAdjacencyList(state):
	'''
	rotates adjacency list by 1
	'''
	state.adjacencyList = state.adjacencyList[1:] + state.adjacencyList[:1]

##### version 2.0
def satisfy(KripkeStructure, ctlStructure):
    '''
    returns set of states that satisfy given ctl property
    '''
    if ctlStructure.getOp() == None:
        return None
    elif ctlStructure.getOp() == CTLOperators.TRUE:
        return KripkeStructure.graphNodeList
    elif ctlStructure.getOp() == CTLOperators.FALSE:
        return None
    elif ctlStructure.getOp() == CTLOperators.AP:
        return satAP(KripkeStructure,ctlStructure.getLabel())
    elif ctlStructure.getOp() == CTLOperators.NOT:
        S1 = satisfy(KripkeStructure,ctlStructure.nextOp1)
        return satNOT(KripkeStructure,S1)
    elif ctlStructure.getOp() == CTLOperators.OR:
        S1 = satisfy(KripkeStructure,ctlStructure.nextOp1)
        S2 = satisfy(KripkeStructure,ctlStructure.nextOp2)
        return satOR(S1,S2)
    elif ctlStructure.getOp() == CTLOperators.EX:
        S1 = satisfy(KripkeStructure,ctlStructure.nextOp1)
        return satEX(KripkeStructure,S1)
    elif ctlStructure.getOp() == CTLOperators.EU:
        S1 = satisfy(KripkeStructure,ctlStructure.nextOp1)
        S2 = satisfy(KripkeStructure,ctlStructure.nextOp2)
        return satEU(KripkeStructure,S1,S2)
    else:
        S1 = satisfy(KripkeStructure,ctlStructure.nextOp1)
        return satEG(KripkeStructure,S1)

def modelCheck(initialState,KripkeStructure,ctlStructure,ctlStructure_pre):
    '''
    This function is lit boiiiiii
    '''

    satisfySet = satisfy(KripkeStructure, ctlStructure)

    if initialState in satisfySet:
        print ctlStructure_pre + " => Property Satisfied!"
    else:
        print ctlStructure_pre + " => Not Satisfied"
        generateCE(KripkeStructure,ctlStructure_pre)

def generateCE(KripkeStructure,ctlStructure_pre):
	'''
	generates the counterexample for a pre-translation sctl structure
	'''
	#Generate kripke sets for counterexample generation
	NStop = ctlStructure_pre[0:2]
	if (NStop == 'EX') or (NStop == 'AX') or (NStop == 'AG') or (NStop == 'AF') or (NStop == 'EF'):
		NSreturn = generateNS(ctlStructure_pre[2:])
		satisfySet = satisfy(KripkeStructure,NSreturn)
	elif (NStop == 'A(') or (NStop == 'E('):
		ctl1,ctl2 = returnUntilStrings(ctlStructure_pre)
		NS1 = generateNS(ctl1)
		NS2 = generateNS(ctl2)
		satisfySet1 = satisfy(KripkeStructure,NS1)
		satisfySet2 = satisfy(KripkeStructure,NS2)

	#Perform counterexample generation
	if NStop == 'EX':
		paths = findEXCounterExample(KripkeStructure,satisfySet,KripkeStructure.graphNodeList[0])
	elif NStop == 'AX':
		paths = findAXCounterExample(KripkeStructure,satisfySet,KripkeStructure.graphNodeList[0])
	elif NStop == 'AG':
		paths = findAGCounterExample(KripkeStructure,satisfySet,KripkeStructure.graphNodeList[0])
	elif NStop == 'AF':
		paths = findAFCounterExample(KripkeStructure,satisfySet,KripkeStructure.graphNodeList[0])
	elif NStop == 'EF':
		paths = findEFCounterExample(KripkeStructure,satisfySet,KripkeStructure.graphNodeList[0])
	elif NStop == 'A(':
		paths = findAUCounterExample(KripkeStructure,satisfySet1,satisfySet2,KripkeStructure.graphNodeList[0])
	elif NStop == 'E(':
		paths = findEUCounterExample(KripkeStructure,satisfySet1,satisfySet2,KripkeStructure.graphNodeList[0])
	else:
		paths = []
		print "Not Supported... yet"
	print 'Counterexample: ' +  str(paths)

def copySet(kripkeSet):
	returnSet = []
	for node in kripkeSet:
		returnSet.append(node)
	return returnSet

if __name__ == '__main__':
	#Generate example with obvious APs
	#f = 'exampleFSM2.vhd'
	f = 'exampleFSM.vhd'
	parser = vhdlParser(f)                          #Instantiates parser
	parser.parseVHDL()                              #Generates .krip file
	KS = parser.returnKripkeStructure()             #creates data structure from .krip file
	KS.addAP(['q','==','1','q'])
	KS.addAP(['p','==','1','p'])

	inputStr = "EF(!p&!q)"
	CTL = generateNS(inputStr)
	#print CTL.returnCTLFormulaString(CTL)
	modelCheck(KS.graphNodeList[0],KS,CTL,inputStr)

	#collection = satisfy(KS,CTL)

	#if collection == None:
	#	print None
	#else:
	#	print returnNodeStackIdList(collection)
	'''
			for state in node.getAdjacencyList():
				if state in collection:
					nodeList.append(state.id)
			print 'Node ' + str(node.id) + ' Outgoing Transitions[to states returned]: ' + str(nodeList)
			nodeList = []
			for state in node.incomingEdges:
				if state in collection:
					nodeList.append(state.id)
			print 'Node ' + str(node.id) + ' Incoming Transitions[to states returned]: ' + str(nodeList)
			print
	'''



    #print KS.getApDictOfDict()
