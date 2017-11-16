from vhdlParser import *
from ctl_ops import *

if __name__ == '__main__':
    #NS = CTLNestedStructure(1,2)
    ns = CTLNestedStructure(CTLOperators.TRUE)
    print ns.getOp()
    #parser = vhdlParser('exampleFSM.vhd')
    #parser.parseVHDL()
    #KS = parser.returnKripkeStructure(parser.filename)
    #print parser.process1
    #Prints references to nodes and their adjacent nodes
    #for index in range(len(KS.graphNodeList)):
    #    print 'Node: ' + str(KS.graphNodeList[index]) + '\nAdj List: ' + str(KS.graphNodeList[index].getAdjacencyList()) + '\n'
    #print KS.addAP(['p','<','1','p'])
    #print KS.ApList
    #for node in KS.graphNodeList:
    #    print node.OutputDict
    #    print node.ApDict
    #print KS.ApDictOfDict
