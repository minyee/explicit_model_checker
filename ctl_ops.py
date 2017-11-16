## Defines the classes for 
import node
import sys
from enum import Enum
from model_checker import *
class CTLOperators(Enum):
	TRUE = 1
	FALSE = 2
	AP = 3
	NOT = 4 # Negation of a propositional logic
	OR = 5
	EX = 6
	EU = 7
	EG = 8




class CTLNestedStructure:
	# initialize with the kind of operation this 
	def __init__(self, operatorsArg, labelArg):
		self.op = operatorsArg
		self.nextOp1 = None
		self.nextOp2 = None
		#self.apDict = apDictArg
		self.label = labelArg
		return

	def addNestedOp(self, nextOp1Arg, nextOp2Arg, labelArg):
		self.nextOp1 = nextOp1Arg
		self.nextOp2 = nextOp2Arg
		self.self = labelArg
		return

	def getOp(self):
		return self.op

	def getNestedOp(self):
		return (self.nextOp1, self.nextOp2)

	def getLabel(self):
		return self.label

	def getAPdict(self):
		return self.apDict


	# def printRecur(self, ctlStruct, string):
	# 	ctlOp1, ctlOp2 = ctlStruct.getNestedOp()
	# 	if ctlStruct.getOp() == CTLOperators.TRUE:
	# 		string += "TRUE"  
	# 	elif ctlStruct.getOp() == CTLOperators.FALSE:
	# 		string += "FALSE"
	# 	elif ctlStruct.getOp() == CTLOperators.AP:
	# 		i = 0
	# 		for key, val in ctlStruct.getAPdict():
	# 			if i > 0:
	# 				string += (" && " + key + "=%d") % val
	# 			else:
	# 				string += ("(" + key + "=%d") % val
	# 				i += 1
	# 		string += ")"
	# 	elif ctlStruct.getOp() == CTLOperators.OR:
	# 		string += ("(" + self.printRecur(self.nextOp1, string) + ") || (" + self.printRecur(self.nextOp2, string) + ")")
	# 	elif ctlStruct.getOp() == CTLOperators.NOT:
	# 		i = 0
	# 		for key, val in ctlStruct.getAPdict():
	# 			if i > 0:
	# 				string += (" && " + key + "=%d") % val
	# 			else:
	# 				string += ("~(" + key + "=%d") % val
	# 				i += 1
	# 		string += ")"
	# 	elif ctlStruct.getOp() == CTLOperators.EX:
	# 		string += "EX("
	# 		string += (printRecur(ctlOp1) + ")")
	# 	elif ctlStruct.getOp() == CTLOperators.EU:
	# 		string += ("E((" + self.printRecur(ctlOp1, string) + ") U (" + self.printRecur(ctlOp2, string) + ")")
	# 	else:
	# 		string += ("EG(" + self.printRecur(ctlOp1, string) + ")")
	# 	return string

	#Transforms a CTL structure into a string formula


def printRecur(ctlStruct):
	if ctlStruct == None:
		return ""
		
	(ctlOp1, ctlOp2) = ctlStruct.getNestedOp()
	string = ""
	if ctlStruct.getOp() == CTLOperators.TRUE:
		string += "TRUE"  
	elif ctlStruct.getOp() == CTLOperators.FALSE:
		string += "FALSE"
	elif ctlStruct.getOp() == CTLOperators.AP:
		i = 0
		for key, val in ctlStruct.getAPdict():
			if i > 0:
				string += (" && " + key + "=%d") % val
			else:
				string += ("(" + key + "=%d") % val
				i += 1
		string += ")"
	elif ctlStruct.getOp() == CTLOperators.OR:
		string += ("(" + printRecur(ctlOp1) + ") || (" + printRecur(ctlOp2) + ")")
	elif ctlStruct.getOp() == CTLOperators.NOT:
		i = 0
		for key, val in ctlStruct.getAPdict():
			if i > 0:
				string += (" && " + key + "=%d") % val
			else:
				string += ("~(" + key + "=%d") % val
				i += 1
		string += ")"
	elif ctlStruct.getOp() == CTLOperators.EX:
		string += "EX("
		string += (printRecur(ctlOp1) + ")")
	elif ctlStruct.getOp() == CTLOperators.EU:
		string += ("E((" + printRecur(ctlOp1) + ") U (" + printRecur(ctlOp2) + ")")
	else:
		string += ("EG(" + printRecur(ctlOp1) + ")")
	return string

def getCTLFormulaString(ctlStructure):
	#string = ""
	print "here"
	return printRecur(ctlStructure)
	#return string
