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