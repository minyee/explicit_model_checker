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
    #turn nodestack into id list
    for node in nodeStack:
        nodeStackList.append(node.id)
    return nodeStackList

def findAUCounterExample(kripkeStructure,kripkeSet1,kripkeSet2,initialState):
    '''
    modified dfs for AU conterexample generation.
	A(KS1 U KS2)
	Runs DFS until it hits a !KS1 before KS2
    '''
    nodeStack = []
    nodeStackList = []
    nodeStack.append(initialState)
    size = len(kripkeStructure.graphNodeList)
    visitedList = [False] * size

    while nodeStack:
        proceed = True
        currNode = nodeStack[len(nodeStack)-1]
        if (currNode in kripkeSet1) or (currNode in kripkeSet2):
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


def findEFCounterExample(ctlSubstring, startStates, kripkeStructure):
	ctlSubstring = '!' + ctlSubstring
	return findAGCounterExample(ctlSubstring, startStates, kripkeStructure)

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
    returnSet = KripkeSet2
    reversedGraph = KripkeStructure.getReversedGraph()
    lastSet = KripkeSet2
    while lastSet:
        currentSet = []
    	for node in lastSet:
			for pointingState in node.incomingEdges:
				if (pointingState in KripkeSet1) and (pointingState not in returnSet):
					currentSet.append(pointingState)
					returnSet.append(pointingState)
        lastSet = currentSet
    return returnSet

def satEG(KripkeStructure, KripkeSet):
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
	returnStates = satEU(KripkeStructure, KripkeSet, returnStates)
	#print returnNodeStackIdList(returnStates)
	return returnStates

def returnNodeStackIdList(nodeStack):
	'''
	prints node stack
	'''
	nodeStackList = []
	#turn nodestack into id list
	for node in nodeStack:
		nodeStackList.append(node.id)
	return nodeStackList

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
	if (NStop == 'EX') or (NStop == 'AX') or (NStop == 'AG'):
		NSreturn = generateNS(ctlStructure_pre[2:])
		satisfySet = satisfy(KripkeStructure,NSreturn)
	elif NStop == 'A(':
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
	elif NStop == 'A(':
		paths = findAUCounterExample(KripkeStructure,satisfySet1,satisfySet2,KripkeStructure.graphNodeList[0])
	else:
		paths = []
		print "Not Supported... yet"
	print 'Counterexample: ' +  str(paths)


if __name__ == '__main__':
	#Generate example with obvious APs
	#f = 'exampleFSM2.vhd'
	f = 'exampleFSM.vhd'
	parser = vhdlParser(f)                          #Instantiates parser
	parser.parseVHDL()                              #Generates .krip file
	KS = parser.returnKripkeStructure()             #creates data structure from .krip file
	KS.addAP(['q','==','1','q'])
	KS.addAP(['p','==','1','p'])


	inputStr = "A(pUq)"
	CTL = generateNS(inputStr)
	#print CTL.returnCTLFormulaString(CTL)
	modelCheck(KS.graphNodeList[0],KS,CTL,inputStr)

	collection = satisfy(KS,CTL)

	if collection == None:
		print None
	else:
		print returnNodeStackIdList(collection)
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
