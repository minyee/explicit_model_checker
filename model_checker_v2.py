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

def dfsAG(kripkeStructure, srcNode, satisfyingStates, paths):
	currNode = srcNode
	nodeStack = []
	size = len(graphNodeList)
	visited = [False] * size
	parent = [None] * size
	nodeStack.append(srcNode)
	visited[currNode.getId()] = True

	path = []
	while len(nodeStack) > 0:
		currNode = nodeStack.pop()
		if currNode not in satisfyingStates:
			while parent[currNode.getId()] != None:
				path.append( currNode.getId() )
			path.reverse()
			paths.append(path)
			return
		visited[currNode.getId()] = True
		for neighbor in currNode.getAdjacencyList():
			#only consider nodes that are in the graphNodeList
			if not visited[neighbor.getId()]:
				nodeStack.append(neighbor)
				parent[neighbor.getId()] = currNode
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
    reversedGraph = kripkeStructure.getReversedGraph()

    for state in KripkeSet:
        currID = state.getId()
        reversedAdjacencyList = reversedGraph[currID].getAdjacencyList()
        for pointingState in reversedAdjacencyList:
            for state in kripkeStructure.graphNodeList:
                if (state.id == pointingState.id) and (state not in returnSet):
                    returnSet.append(state)
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
            reversedAdjacencyList = reversedGraph[node.id].getAdjacencyList()
            for pointingState in reversedAdjacencyList:
                for state in KripkeStructure.graphNodeList:
                    if (state.id == pointingState.id) :
                        if (state in KripkeSet1) and (state not in returnSet):
                            currentSet.append(state)
                            returnSet.append(state)
        lastSet = currentSet
    return returnSet

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
    idList = []

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
    NStop = ctlStructure_pre[0:2]
    NSreturn = generateNS(ctlStructure_pre[2:])
    satisfySet = satisfy(KripkeStructure,NSreturn)

    if NStop == 'EX':
        paths = findEXCounterExample(KripkeStructure,satisfySet,KripkeStructure.graphNodeList[0])
    if NStop == 'AX':
        paths = findAXCounterExample(KripkeStructure,satisfySet,KripkeStructure.graphNodeList[0])
    if NStop == 'AG':
        paths = findAGCounterExample(KripkeStructure,satisfySet,KripkeStructure.graphNodeList[0])
    else:
        paths = []
        print "Not Supported... yet"
    print 'Counterexample: ' +  str(paths)


if __name__ == '__main__':
    #Generate example with obvious APs
    f = 'exampleFSM.vhd'
    parser = vhdlParser(f)                          #Instantiates parser
    parser.parseVHDL()                              #Generates .krip file
    KS = parser.returnKripkeStructure()             #creates data structure from .krip file
    KS.addAP(['q','==','1','q'])
    KS.addAP(['p','==','1','p'])

    inputStr = "AG!(p&q)"
    CTL = generateNS(inputStr)
    #print CTL.returnCTLFormulaString(CTL)

    modelCheck(KS.graphNodeList[0],KS,CTL,inputStr)

'''
    collection = satisfy(KS,CTL)
    if collection == None:
        print None
    else:
        for node in collection:
            print node.id
'''

    #print KS.getApDictOfDict()
