## Defines the classes for
import node
import sys
from enum import Enum
from model_checker import *
class CTLOperators(Enum):
	NULL = 0
	TRUE = 1
	FALSE = 2
	AP = 3
	NOT = 4
	OR = 5
	EX = 6
	EU = 7
	EG = 8

class CTLNestedStructure:
	'''
	CTL Nested Structue. Each instantiation represents a separate operator.
	Only the OR and EU operators utilize both nextOps
	Only the AP operator utilizes the label
	'''
	# initialize with the kind of operation this
	def __init__(self, operatorsArg):
		self.op = operatorsArg
		self.nextOp1 = None
		self.nextOp2 = None
		self.label = None
		return

	def addNestedOp(self, nextOp1, nextOp2):
		self.nextOp1 = nextOp1
		self.nextOp2 = nextOp2
		return

	def addLabel(self,label):
		self.label = label

	def getOp(self):
		return self.op

	def getNestedOp(self):
		return (self.nextOp1, self.nextOp2)

	def getLabel(self):
		return self.label

	def getCTLFormulaString(self):
		string = self.returnCTLFormulaString(self)
		return string
	#Transforms a CTL structure into a string formula
	def returnCTLFormulaString(self,op):
		'''
	    prints formula using nested structure
	    '''
	   	string = ''
	   	if op.getOp() == CTLOperators.AP:#terminalCase
			string += op.label
	   	elif op.getOp() == CTLOperators.EU:
			string += 'E(' + self.returnCTLFormulaString(op.nextOp1) + 'U' + self.returnCTLFormulaString(op.nextOp2) + ')'
	  	elif op.getOp() == CTLOperators.OR:
			string += '(' + self.returnCTLFormulaString(op.nextOp1) + '|' + self.returnCTLFormulaString(op.nextOp2) + ')'
	   	elif op.getOp() == CTLOperators.EX:
			string += 'EX' + self.returnCTLFormulaString(op.nextOp1)
	   	elif op.getOp() == CTLOperators.EG:
			string += 'EG' + self.returnCTLFormulaString(op.nextOp1)
	   	elif op.getOp() == CTLOperators.NOT:
			string += '!' + self.returnCTLFormulaString(op.nextOp1)
	   	return string
