from node import *

## AP is the abbreviation for atomic proposition

class State(Node):
	def __init__(self, stateID, APdictArg):
		Node.__init__(self,stateID)
		self.APdict = APdictArg

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
	def __init__(self, graphNodeListArg, ApDictOfDict):
		Graph.__init__(self,graphNodeListArg)
		self.ApDictOfDict = ApDictOfDict
