## Defines the classes for 
import node
from enum import enum

class CTLOperators(Enum):
	TRUE = 1
	FALSE = 2
	AP = 3
	NOTAP = 4 # Negation of a propositional logic
	OR = 5
	EX = 6
	EU = 7
	EG = 8


class CTLNestedStructure:
	# initialize with the kind of operation this 
	def __init__(self, operatorsArg, apDictArg):
		self.op = operatorsArg
		self.nextOp1 = None
		self.nextOp2 = None
		self.apDict = apDictArg
		return

	def addNestedOp(self, nextOp1Arg, nextOp2Arg, apDictArg):
		self.nextOp1 = nextOp1
		self.nextOp2 = nextOp2
		self.apDict = apDictArg
		return

	def getOp(self):
		return self.op

	def getNestedOp(self):
		return (self.nextOp1, self.nextOp2)

	def getAPdict(self):
		return self.apDict

	def printRecur(self, ctlStruct, string):
		ctlOp1, ctlOp2 = ctlStruct.getNestedOp()
		if ctlStruct.getOp() == TRUE:
			string += "TRUE"  
		elif ctlStruct.getOp() == FALSE:
			string += "FALSE"
		elif ctlStruct.getOp() == AP:
			i = 0
			for key, val in ctlStruct.getAPdict():
				if i > 0:
					string += (" && " + key + "=%d") % val
				else:
					string += ("(" + key + "=%d") % val
					i += 1
			string += ")"
		elif ctlStruct.getOp() == OR:
			string += ("(" + printRecur(self.nextOp1) + ") || (" printRecur(self.nextOp2) + ")")
		elif ctlStruct.getOp() == NOTAP
			i = 0
			for key, val in ctlStruct.getAPdict():
				if i > 0:
					string += (" && " + key + "=%d") % val
				else:
					string += ("~(" + key + "=%d") % val
					i += 1
			string += ")"
		elif ctlStruct.getOp() == EX:
			string += "EX("
			string += (printRecur(ctlOp1) + ")")
		elif ctlStruct.getOp() == EU:
			string += ("E((" + printRecur(ctlOp1) + ") U (" + printRecur(ctlOp2) + ")")
		else:
			string += ("EG(" + printRecur(ctlOp1) + ")")
		return string

	#Transforms a CTL structure into a string formula
	def getCTLFormulaString(self):
		string = ""
		printRecur(self, string)
		return string