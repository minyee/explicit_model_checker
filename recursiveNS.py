from ctl_ops import *
import re

def generateNS(CTLString):
    '''
    Generates nested structure given a properly formed CTL string
        E(                  => Implies EU
        (                   => Implies OR
        lowercase string    => implies AP
        EG                  => EG
        EX                  => EX
        !                   => NOT
    '''
    if CTLString[0] == 'E':
        nextChar = CTLString[1]
        if nextChar == '(':                                     #Assume EU is seen
            str1,str2 = returnUntilStrings(CTLString)
            arg1 = generateNS(str1)                             #recursive call for arg1
            arg2 = generateNS(str2)                             #recursive call for arg2
            returnVal = CTLNestedStructure(CTLOperators.EU)     #Generate EU operator
            returnVal.addNestedOp(arg1,arg2)                    #Add ops that were found recursively
            return returnVal                                    #return EU w/ args that are the returned objects
        elif nextChar == 'G':
            arg1 = generateNS(CTLString[2:])                    #recursive call on everything to the right of EG
            returnVal = CTLNestedStructure(CTLOperators.EG)     #Generate EG operator
            returnVal.addNestedOp(arg1,None)                    #Add op that was found recursively
            return returnVal                                    #return EG structure that points to returned above object
        elif nextChar == 'X':
            arg1 = generateNS(CTLString[2:])                    #recursive call on everything to the right of EX
            returnVal = CTLNestedStructure(CTLOperators.EX)     #Generate EX operator
            returnVal.addNestedOp(arg1,None)                    #Add op that was found recursively
            return returnVal                                    #return EX structure that points to returned above object
        elif nextChar == 'F':                                   # Translation => EFp = E(TRUEUp)
            arg1 = generateNS(CTLString[2:])                    #recursive call on everything to the right of EF
            returnVal = CTLNestedStructure(CTLOperators.EU)     #create top op for translation
            trueVal = CTLNestedStructure(CTLOperators.TRUE)     #intermediate op
            returnVal.addNestedOp(trueVal,arg1)                 #generate EF operator
            return returnVal                                    #return translated nested structure
        else:
            print "Invalid Formula"                             #Invalid if it gets here
            return                                              #returns to end generateNSion call
    elif CTLString[0] == 'A':
        nextChar = CTLString[1]
        if nextChar == '(':                                     #A(pUq)
            str1,str2 = returnUntilStrings(CTLString)
            arg1 = generateNS(str1)                             #recursive call for arg1
            arg2 = generateNS(str2)                             #recursive call for arg2
            #Top
            returnVal = CTLNestedStructure(CTLOperators.NOT)     #Generate NOT operators
            orVal1 = CTLNestedStructure(CTLOperators.OR)        #Generate first or
            #Left
            leftVal = CTLNestedStructure(CTLOperators.EU)
            notVal1 = CTLNestedStructure(CTLOperators.NOT)
            orVal2 = CTLNestedStructure(CTLOperators.OR)
            notVal2 = CTLNestedStructure(CTLOperators.NOT)
            #Right
            rightVal = CTLNestedStructure(CTLOperators.EG)
            notVal3 = CTLNestedStructure(CTLOperators.NOT)
            #Construct Right Val
            notVal3.addNestedOp(arg2,None)
            rightVal.addNestedOp(notVal3,None)
            #Construct Left Value
            orVal2.addNestedOp(arg1,arg2)
            notVal2.addNestedOp(orVal2,None)
            notVal1.addNestedOp(arg2,None)
            leftVal.addNestedOp(notVal1,notVal2)
            #returnVal!
            orVal1.addNestedOp(leftVal,rightVal)
            returnVal.addNestedOp(orVal1,None)                    #Add ops that were found recursively
            return returnVal
        elif nextChar == 'G':
            arg1 = generateNS(CTLString[2:])                    #recursive call on everything to the right of AF
            returnVal = CTLNestedStructure(CTLOperators.NOT)    #create top op for translation
            euVal = CTLNestedStructure(CTLOperators.EU)         #intermediate op
            notVal = CTLNestedStructure(CTLOperators.NOT)       #bottom op for translation. points to arg 1
            notVal.addNestedOp(arg1,None)
            euVal.addNestedOp(CTLNestedStructure(CTLOperators.TRUE),notVal)
            returnVal.addNestedOp(euVal,None)                   #Generate AG operator
            return returnVal                                    #return translated nested structure
        elif nextChar == 'X':
            arg1 = generateNS(CTLString[2:])                    #recursive call on everything to the right of AF
            returnVal = CTLNestedStructure(CTLOperators.NOT)    #create top op for translation
            exVal = CTLNestedStructure(CTLOperators.EX)         #intermediate op
            notVal = CTLNestedStructure(CTLOperators.NOT)       #bottom op for translation. points to arg 1
            notVal.addNestedOp(arg1,None)
            exVal.addNestedOp(notVal,None)
            returnVal.addNestedOp(exVal,None)                   #Generate AX operator
            return returnVal                                    #return translated nested structure
        elif nextChar == 'F':                                   # Translation => AFp = !EG!p
            arg1 = generateNS(CTLString[2:])                    #recursive call on everything to the right of AF
            returnVal = CTLNestedStructure(CTLOperators.NOT)    #create top op for translation
            egVal = CTLNestedStructure(CTLOperators.EG)         #intermediate op
            notVal = CTLNestedStructure(CTLOperators.NOT)       #bottom op for translation. points to arg 1
            notVal.addNestedOp(arg1,None)
            egVal.addNestedOp(notVal,None)
            returnVal.addNestedOp(egVal,None)                   #Generate AF operator
            return returnVal                                    #return translated nested structure
        else:
            print "Invalid Formula"                             #Invalid if it gets here
            return                                              #returns to end generateNSion call
    elif CTLString[0] == '!':                                   #If we see a NOT operator
        arg1 = generateNS(CTLString[1:])                        #recursive call on the rest of the string
        returnVal = CTLNestedStructure(CTLOperators.NOT)        #Generate Not operator
        returnVal.addNestedOp(arg1,None)                        #Add op that was found recursively
        return returnVal                                        #return not pointing to object that was return in above line
    elif CTLString[0] == '(':                                   #If we see an OR,TRUE, or FALSE operator
        if CTLString[1] == 'T':                                 #TERMINAL CASE (TRUE)
            returnVal = CTLNestedStructure(CTLOperators.TRUE)
            return returnVal
        elif CTLString[1] == 'F':                               #TERMINAL CASE (FALSE)
            returnVal = CTLNestedStructure(CTLOperators.FALSE)
            return returnVal
        else:
            str1,str2 = returnOr_AndStrings(CTLString)                  #first string is contained to left side of | to first (
            arg1 = generateNS(str1)                                     #recursive call for arg1
            arg2 = generateNS(str2)                                     #recursive call for arg2
            if returnOpType(CTLString):
                returnVal = CTLNestedStructure(CTLOperators.OR)         #Generate EU operator
                returnVal.addNestedOp(arg1,arg2)                        #Add ops that were found recursively
            else:                                                       #Assume that AND is seen
                returnVal = CTLNestedStructure(CTLOperators.NOT)
                orVal = CTLNestedStructure(CTLOperators.OR)
                notVal1 = CTLNestedStructure(CTLOperators.NOT)
                notVal2 = CTLNestedStructure(CTLOperators.NOT)
                notVal1.addNestedOp(arg1,None)
                notVal2.addNestedOp(arg2,None)
                orVal.addNestedOp(notVal1,notVal2)
                returnVal.addNestedOp(orVal,None)
            return returnVal
    #elif CTLString == 'p' or CTLString == 'q':                  #TERMINAL CASE
    elif re.match('^[a-z]+$',CTLString) is not None:            #if only lowercase letters assume AP
    #elif CTLString in returnApNames():                         #TERMINAL CASE
        returnVal = CTLNestedStructure(CTLOperators.AP)         #Create AP Op
        returnVal.addLabel(CTLString)                           #Add label
        return returnVal                                        #Return AP op
    else:
        print "Invalid Formula"

def returnOr_AndStrings(string):
    '''
    Returns reference to list of two strings that OR operator operates on
    [start:end] => items start through end-1
    '''
    counterOpen = 0
    counterClosed = 0
    string = string[1:len(string)-1]#strip off outer parantheses
    for index,char in enumerate(string):
        if char == '(':
            counterOpen += 1
        if char == ')':
            counterClosed += 1
        elif char == '|' or char == '&':
            if counterOpen == counterClosed:
                return [string[:index],string[index+1:]]

def returnUntilStrings(string):
    '''
    Returns reference to list of two strings that EU operator operates on
    [start:end] => items start through end-1
    '''
    counterOpen = 0
    counterClosed = 0
    string = string[2:len(string)-1]#strip off outer parantheses and beginning E/A
    for index,char in enumerate(string):
        if char == '(':
            counterOpen += 1
        if char == ')':
            counterClosed += 1
        elif char == 'U':
            if counterOpen == counterClosed:
                return [string[:index],string[index+1:]]

def returnOpType(string):
    '''
    Returns True for OR and False for AND
    '''
    counterOpen = 0
    counterClosed = 0
    string = string[2:len(string)-1]#strip off outer parantheses and beginning E/A
    for index,char in enumerate(string):
        if char == '(':
            counterOpen += 1
        if char == ')':
            counterClosed += 1
        elif char == '|':
            if counterOpen == counterClosed:
                return True
        elif char == '&':
            if counterOpen == counterClosed:
                return False

if __name__ == "__main__":
    #topOp = generateNS('!AX(EXAF(p|q)|E((FALSE)Uq))')
    topOp = generateNS('A(pUq)')
    print topOp.getCTLFormulaString()
