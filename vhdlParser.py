#Author: Erik Anderson
#Date: 11/8/2017
#Description:

import re
from node import *
from kripke_structure import *

class vhdlParser:
    def __init__(self,filename):
        '''
        VHDL Parser class
        Assumptions (all can be fixed but leave in for now):
            1. First two processes are FSM processes (does not matter the order)
            2. 'rising_edge' string is not used for anything besides the event
            3. All outputs defined for each state.
            4. Processes list states in same order.
            5. RESET NOT INCLUDED
        '''
        self.filename = filename.strip('.krip').strip('.vhd')
        self.process1 = []
        self.process2 = []
        self.states = []
        #Number of states [Integer]
        self.numStates = 0
        #All APs present in system [List of strings]
        self.APs = []
        #Outputs/values of APs of each state [list of dictionaries (key => AP, val => value)]
        self.outputs = []
        #Transitions from each state to [list of states that state can transition to]
        self.transitions = []

    def parseVHDL(self):
        self.captureProcesses()
        self.parseProcesses()
        self.generateKrip()

    def captureProcesses(self):
        '''
        Returns lists according to each line of the first two processes
        '''
        f = open(self.filename + '.vhd','r')
        #Read lines until get to first process statement
        processStart = []
        processEnd = []
        doc = []
        for i, line in enumerate(f):
            #Get rid of \n, \t, and make all text lowercase
            line = line.replace('\n','').replace('\t','').lower()
            #Get rid of comments
            line = line.split('--', 1)[0]
            #Search for lines with process w/o end
            doc.append(line)
            if 'process' in line and 'end process' not in line:
                processStart.append(i)
            elif 'end process' in line:
                processEnd.append(i+1)

        for i in range(processStart[0],processEnd[0]):
            self.process1.append(doc[i])
        for i in range(processStart[1],processEnd[1]):
            self.process2.append(doc[i])
        f.close()

    def parseProcesses(self):
        '''
        Parses process list (pType => 0 (transition), pType => 1 (output))
        Returns transitions and number of states if transition process
        Returns list of APs and output for each state if output process
        '''
        p1 = ''
        p2 = ''
        for item in self.process1:
            p1 += item
        for item in self.process2:
            p2 += item

        if 'rising_edge' in p1:
            self.parseTransition(self.process1)
            self.parseOutput(self.process2)
        else:
            self.parseTransition(self.process2)
            self.parseOutput(self.process1)

    def parseOutput(self,process):
        states = []
        whenLines = []
        numStates = 0
        outputsTest = []
        #Gathers state names and number of states
        for i,item in enumerate(process):
            if 'when' in item:
                numStates += 1
                states.append(item.replace(' ','').replace('=>','').split('when', 1)[1])
                whenLines.append(i)
        whenLines.append(len(process)-1)
        #Iterate through all of the states transitions
        for i in range(self.numStates):
            outputDict = {}
            #Find end states for states
            for j in range(whenLines[i],whenLines[i+1]):
                #construct transition string for .krip file
                if '<=' in process[j]:
                    key = process[j].replace(' ','').replace(';','').split('<=')[0]
                    value = process[j].replace(' ','').replace(';','').replace('\'','').split('<=')[1]
                    outputDict[key] = value
            self.outputs.append(outputDict)
        for key in self.outputs[0].keys():
            self.APs.append(key)
        if states != self.states or numStates != self.numStates:
            print "Error! numStates and/or states different (ordering also triggers this warning as of now)"

    def parseTransition(self,process):
        whenLines = []
        stateDict = {}
        #Gathers state names and number of states
        for i,item in enumerate(process):
            if 'when' in item:
                self.numStates += 1
                self.states.append(item.replace(' ','').replace('=>','').split('when', 1)[1])
                whenLines.append(i)
        whenLines.append(len(process)-1)
        #Construct dictionary
        for k,item in enumerate(self.states):
            stateDict[k] = item
        #Iterate through all of the states transitions
        for i in range(self.numStates):
            endStates = []
            #Find end states for states
            for j in range(whenLines[i],whenLines[i+1]):
                #construct transition string for .krip file
                if '<=' in process[j]:
                    #endStates.append(process[j].replace(' ','').replace(';','').split('<=')[1])
                    endStates.append(stateDict.keys()[stateDict.values().index(process[j].replace(' ','').replace(';','').split('<=')[1])])
            #Construct string that will be written to .krip file
            endStates.sort()
            self.transitions.append(endStates)

    def generateKrip(self):
        f = open(self.filename + '.krip','w')
        #Write numStates to file
        f.write(str(self.numStates))
        f.write('\n')
        #Write APs to file
        for i in range(len(self.APs)):
            if i < len(self.APs) - 1:
                f.write(self.APs[i] + ',')
            else:
                f.write(self.APs[i])
        #f.write(self.APs[len(self.APs) - 1])
        f.write('\n')
        #Write AP values to file
        for j in range(self.numStates):
            f.write(str(j)+':'+str(self.outputs[j]).replace('\'','').replace('\"',''))
            f.write('\n')
            f.write(str(self.transitions[j]).replace('[','').replace(']','').replace(' ',''))
            f.write('\n')
        f.close()

    def returnKripkeStructure(self):
    	'''
    	Returns List of State objects used to Initialize kripke structure. Uses .krip file to extract info
    		State __init__(self, stateID, adjacencyList, APdictArg):
    			.APdict => key => AP, val => value of AP
    			.ID => stateID
    			.adjacency list => sublist of full list of nodes
    	'''
        graphNodeList = [] #id(key) returns state object(value)
        ApDictOfDict = {} #id(key) returns dictionary of APs
        ApDict = {}
        adjacencyList = []
        adjacencyDict = {}

        f = open(self.filename + '.krip','r')
        #First two lines are not needed
        numStates = int(f.readline().strip('\n'))
        APs = f.readline()
        APs = APs.strip('\n').split(',')
        for line in f:
            if '{' in line:
                #Generate stateID and APDictofDict
                stateID = int(line.split(':')[0])
                line = line.strip('\n').replace('}','').replace('{','').replace(' ','').replace(',',':').split(':')[1:len(line)-1]
                ApDictOfDict[stateID] = {}
                for i in range(len(line)):
                    if i % 2 == 0:
                        ApDictOfDict[stateID][line[i]] = line[i+1]
            else:
                adjacencyList = []
                line = line.strip('\n').split(',')
                for i in range(len(line)):
                    line[i] = int(line[i])
                    adjacencyList.append(line[i])
                adjacencyDict[stateID] = adjacencyList

        for i in range(numStates):
            graphNodeList.append(State(i,ApDictOfDict[i]))
        for i in range(numStates):
            for item in adjacencyDict[i]:
                graphNodeList[i].addNeighborNode(graphNodeList[item])
        incomingEdgeDict = {}
        for state in graphNodeList:
            incomingEdgeDict[state.id] = []
        for state in graphNodeList:
            for node in state.getAdjacencyList():
                incomingEdgeDict[node.id].append(state)
        for key in incomingEdgeDict:
            for node in incomingEdgeDict[key]:
                graphNodeList[key].addIncomingEdge(node)
        return KripkeStructure(graphNodeList,ApDictOfDict)
