from vhdlParser import *

if __name__ == '__main__':
    parser = vhdlParser('exampleFSM')
    KS = parser.returnKripkeStructure('exampleFSM')

    #Prints references to nodes and their adjacent nodes
    for index in range(len(KS.graphNodeList)):
        print 'Node: ' + str(KS.graphNodeList[index]) + '\nAdj List: ' + str(KS.graphNodeList[index].getAdjacencyList()) + '\n'
