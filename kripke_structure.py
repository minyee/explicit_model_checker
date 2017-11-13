import node

## AP is the abbreviation for atomic proposition

class State(Node):
	def __init__(self, id, APdictArg):
		super().__init__(id)
		self.APdict = APdictArg
		return

	def __init__(self, id, adjacencyList, APdictArg):
		super().__init__(id, adjacencyList)
		self.APdict = APdictArg
		return 

	# Checks if this state in the Kripke structure satisfies the 
	# atomic propositions
	def satisfyAP(self, apDict)
		satisfy = True
		for key, val in apDict.items():
			if self.APdict.has_key(key)
				satisfy = satisfy and (self.APdict[key] ^ val)
		return satisfy

class KripkeStructure(Graph):
	def __init__(self, graphNodeListArg, ApDictOfDict):
		theGraph = super().__init__(graphNodeListArg)
		for key, apDict in ApDictOfDict:
			kripkeState = State(key, )
		return self
