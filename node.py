import copy
import sys

class Node:
	def __init__(self, stateID):
		self.adjacencyList = []
		self.numNeighbors = len(self.adjacencyList)
		self.id = stateID

	def getId(self):
		return self.id

	def addNeighborNode(self, newNode):
		if newNode != None:
			self.adjacencyList.append(newNode)
			self.numNeighbors += 1
		return

	def getAdjacencyList(self):
		return self.adjacencyList

	# Checks if a node is a neighbor to the current node
	def isNeighbor(self, nodeOfInterest):
		for someNode in self.adjacencyList:
			if someNode.getId() == nodeOfInterest.getId():
				return True
		return False


class Graph:
	def __init__(self, graphNodeList):
		self.numNodes = len(graphNodeList)
		self.graphNodeList = graphNodeList # This is the forward graph
		#self.reverseGraph = None
		self.reversedGraph = []
		self.reverseGraph()

	# Given the node id, returns the node reference
	def getNode(self, nodeID):
		for node in self.graphNodeList:
			if node.getId() == nodeID:
				return node
		return None

	def getGraphNodeList(self):
		return self.graphNodeList

	def reverseGraph(self):
		reversedG = {}
		graphSize = len(self.graphNodeList)
		## Initialize the reverse graph
		for i in range(graphSize):
			reversedG[i] = Node(i)

		for node in self.graphNodeList:
			currNodeID = node.getId()
			for neighborNode in node.getAdjacencyList():
				neighborNodeID = neighborNode.getId()
				reversedG[neighborNodeID].addNeighborNode(reversedG[currNodeID])
		self.reversedGraph = [0] * graphSize
		for i in range(graphSize):
			node = reversedG[i]
			self.reversedGraph[i] = node
		return self

	def getReversedGraph(self):
		return self.reversedGraph

	def getReversedGraphNeighborList(src):
		for i in range(self.numNodes):
			if src == self.graphNodeList[i].getId():
				return self.reverseGraph[i].getAdjacencyList
		return None

	def findReversedPath(self, srcNode, dstNode):
		srcId = srcNode.getId()
		dstId = dstNode.getId()
		# This method is not finished


	def findCycleRecursive(self, currNode, discoverTime, low, inStackBool, stack, time, CycleCollection):
		currNodeID = currNode.getId()
		time += 1
		discoverTime[currNodeID] = low[currNodeID] = time
		inStackBool[currNodeID] = True
		stack.append(currNode)
		
		
		for neighborNode in currNode.getAdjacencyList():
			neighborNodeID = neighborNode.getId()
			# Case 1: neighbor has not been visited, recur on it
			#print neighborNodeID
			if discoverTime[neighborNodeID] < 0:
				time = self.findCycleRecursive(neighborNode, discoverTime, low, inStackBool, stack, time, CycleCollection)
				low[currNodeID] = min(low[currNodeID], low[neighborNodeID])	
			elif inStackBool[neighborNodeID]:
			#Case 2: neighbor has been visited
			# if visited and is still in stack, then we have a back edge
				low[currNodeID] = min(discoverTime[neighborNodeID], low[currNodeID])

		cycle = []
		if low[currNodeID] == discoverTime[currNodeID]:
			while len(stack) > 0:
				tmpNode = stack.pop()
				tmpNodeID = tmpNode.getId()
				if tmpNodeID != currNodeID:
					cycle.append(tmpNode)	
				else:
					cycle.append(tmpNode)
					break
		if len(cycle) > 1:
			CycleCollection.append(cycle)
		return time

	# Uses Tarjan to find SCC
	def findSCC(self):
		stack = []
		low = [-1] * len(self.graphNodeList)
		discoverTime = [-1] * len(self.graphNodeList)
		inStackBool = [False] * len(self.graphNodeList)
		CycleCollection = []
		time = 0
		for i in range(len(self.graphNodeList)):
			if discoverTime[i] < 0:
				self.findCycleRecursive(self.graphNodeList[i], discoverTime, low, inStackBool, stack, time, CycleCollection)
		return CycleCollection


	def findSubGraphSCC(self, SubGraph):
		#firstNode = copy.copy(self.graphNodeList[0])
		visitedNode = {} #maps node by id and see if they have been visited

		for node in SubGraph:
			visitedNode[node.getId()] = tuple(-1, node.getId())
		time = 0
		nodeStack = [SubGraph[0]]
		numNodes = length(SubGraph)
		while not nodeStack.empty():
			foundCycle = False
			ancestorID = sys.maxint
			currNode = nodeStack.pop()
			(currNodeVisitedTime, currNodeLowestAncestor) = visitedNode[currNode.getId()]
			nodeNeighbors = currNode.getAdjacencyList()
			for neighborNode in nodeNeighbors:
				neighborNodeID = neighborNode.getId()
				(visitedTime,lowestID) = visitedNode[neighborNodeID]
				if (visitedTime < 0): # this node has been visited before
					#visitedNode[neighborNode.getId()] =
					visitedNode[neighborNodeID] = tuple(visitedNode, min(currNodeLowestAncestor, lowestID))
					nodeStack.append(neighborNode)
				else:
					#figure out if this is an upward edge in the tree
					if visitedTime < time:
						# found an SCC
						ancestorID = min(lowestID, currNodeLowestAncestor)
						foundCycle = True
			if foundCycle:
				visitedNode[currNode.getId()] = tuple(time,ancestorID)
			else:
				visitedNode[currNode.getId()] = tuple(time,currNodeLowestAncestor)
			time += 1

		commonAncestors = {}
		SCCs = []
		## Now find all nodes with common ancestors
		for i in range(visitedNode.size()):
			(timeVisited, ancestor) = visitedNode[i]
			if commonAncestors[ancestor] == None:
				#no ancestors
				commonAncestors[ancestor] = [i]
			else:
				commonAncestors[ancestor].append(i)
		## Finally populate these nodes into SCC, ignoring SCC's with only 1 node
		for aList in commonAncestors:
			if aList.size() > 1:
				SCCs.append(aList)
		return SCCs
