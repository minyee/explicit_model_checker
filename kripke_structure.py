from node import *

## AP is the abbreviation for atomic proposition

class State(Node):
	def __init__(self, stateID, OutputDictArg):
		Node.__init__(self,stateID)
		self.OutputDict = OutputDictArg
		#Initialize to be empty
		self.ApDict = {}

	def satisfyAP(self, apDict):
		'''
		Checks if this state in the Kripke structure satisfies the APs
		'''
		satisfy = True
		for key, val in apDict.items():
			if self.APdict.has_key(key):
				satisfy = satisfy and (self.APdict[key] ^ val)
		return satisfy

class KripkeStructure(Graph):
	def __init__(self, graphNodeListArg, OutputDictOfDict):
		Graph.__init__(self,graphNodeListArg)
		self.OutputDictOfDict = OutputDictOfDict
		#Initialize to be empty
		self.ApDictOfDict = {}
		self.ApList = []

	def addAP(self,ApDefinition):
		'''
		Given an AP definition ([outputName,conditionalOperator,outputVal,ApName])
		adds an AP to the APDictofDict. Returns False if it doesnt work...
		'''
		#Vars created for clarity
		outputName = ApDefinition[0]
		conditionalOperator = ApDefinition[1]
		outputVal = ApDefinition[2]
		ApName = ApDefinition[3]
		#Add ApDict to each node AND generate ApDictOfDict for KS
		if outputName in self.OutputDictOfDict[0]:
			for node in self.graphNodeList:
				self.ApDictOfDict[node.id] = {}
				if conditionalOperator == "==":
					if int(self.OutputDictOfDict[node.id][outputName]) == int(outputVal):
						self.ApDictOfDict[node.id][ApName] = True
						node.ApDict = self.ApDictOfDict[node.id]
					else:
						self.ApDictOfDict[node.id][ApName] = False
						node.ApDict = self.ApDictOfDict[node.id]
				elif ApDefinition[1] == ">":
					if int(self.OutputDictOfDict[node.id][outputName]) > int(outputVal):
						self.ApDictOfDict[node.id][ApName] = True
						node.ApDict = self.ApDictOfDict[node.id]
					else:
						self.ApDictOfDict[node.id][ApName] = False
						node.ApDict = self.ApDictOfDict[node.id]
				elif ApDefinition[1] == "<":
					if int(self.OutputDictOfDict[node.id][outputName]) < int(outputVal):
						self.ApDictOfDict[node.id][ApName] = True
						node.ApDict = self.ApDictOfDict[node.id]
					else:
						self.ApDictOfDict[node.id][ApName] = False
						node.ApDict = self.ApDictOfDict[node.id]
				else:
					print "Invalid Conditional Operator"
					return False
		else:
			print "Invalid Output Specified"
			return False
		#Keep a list of all the APs attached to the KS
		self.ApList.append(ApDefinition)
		return True
