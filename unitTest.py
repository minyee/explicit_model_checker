from model_checker import *
from node import *
from ctl_ops import *
from recursiveNS import *
#from enum import enum

print "Hello, this is the start of the unit tests for model_checker"
numNodes = 10
nodesArray1 = [0] * numNodes

for i in range(numNodes):
	nodesArray1[i] = Node(i)
	print "The id for this node is: %d" % nodesArray1[i].getId()

for i in range(numNodes):
	nodesArray1[i].addNeighborNode(nodesArray1[(i + 1) % numNodes])

for i in range(numNodes):
	neighbors = nodesArray1[i].getAdjacencyList()
	string = "Node %d has neighbor " % i
	for neighbor in neighbors:
		string += ("%d " % neighbor.getId())
		#nodesArray1[i].addNeighborNode(nodesArray1[(i + 1) % numNodes])
	print string

graph1 = Graph(nodesArray1)


nodesArray1[3].addNeighborNode(nodesArray1[5])
node3 = graph1.getNode(3)

string = "Node 3 in graph1 has neighbors: "
for neighbor in node3.getAdjacencyList():
	string += ("Node %d ") % neighbor.getId()
print string


print "Testing graph1's reversedGraph"
reversedGraph1 = graph1.getReversedGraph()
print reversedGraph1
for nodeReversed in reversedGraph1:
	currId = nodeReversed.getId()
	print "Curr Reversed Node: %d has neighbors: " % currId 
	tmpstring = ""
	for neighborReversed in nodeReversed.getAdjacencyList(): 
		tmpstring += " Node %d" % neighborReversed.getId()
	print tmpstring

	

print "Now check parserCTL"
#ctl1 = "E(EG(T))U((EX(F))|(T))"
ctl1 = "!EG(EX(p|q)|E(pUq))"
topOp = generateNS(ctl1)
print topOp.getCTLFormulaString()
#stateSet = satisfy(topOp)



print "Testing Graph Algorithms"
numNodes = 5
nodesArray2 = [0] * numNodes
for i in range(numNodes):
	nodesArray2[i] = Node(i)
for i in range(numNodes):
	nodesArray2[i].addNeighborNode(nodesArray2[(i + 1) % numNodes])
graph2 = Graph(nodesArray2)
sccs = graph2.findSCC()
for cycle in sccs:	
	string = ""
	for node in cycle:
		string += (str(node.getId()) + " ")
	string += "\n"
	print "The cycle has: " + string

numNodes = 6
nodesArray3 = [0] * numNodes
for i in range(numNodes):
	nodesArray3[i] = Node(i)
nodesArray3[0].addNeighborNode(nodesArray3[1])
nodesArray3[1].addNeighborNode(nodesArray3[2])
nodesArray3[2].addNeighborNode(nodesArray3[0])
nodesArray3[2].addNeighborNode(nodesArray3[3])
nodesArray3[3].addNeighborNode(nodesArray3[4])
nodesArray3[3].addNeighborNode(nodesArray3[5])
nodesArray3[4].addNeighborNode(nodesArray3[0])
nodesArray3[5].addNeighborNode(nodesArray3[3])
graph3 = Graph(nodesArray3)
sccs3 = graph3.findSCC()
for cycle in sccs3:	
	string = ""
	for node in cycle:
		string += (str(node.getId()) + " ")
	string += "\n"
	print "The cycle has: " + string
print "Completed model_checker unit test, goodbye"