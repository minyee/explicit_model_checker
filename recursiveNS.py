from ctl_ops import *

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
        if nextChar == '(':
            #######################################################################################################################
            #######################################################################################################################
            str1,str2 = returnUntilStrings(CTLString)
            #######################################################################################################################
            #######################################################################################################################
            arg1 = generateNS(str1)                             #recursive call for arg1
            arg2 = generateNS(str2)                             #recursive call for arg2
            returnVal = CTLNestedStructure(CTLOperators.EU)     #Generate EU operator
            returnVal.addNestedOp(arg1,arg2)                    #Add ops that were found recursively
            return returnVal                                    #return EU w/ args that are the returned objects
        elif nextChar == 'G':
            arg1 = generateNS(CTLString[3:len(CTLString) - 1])  #recursive call on everything to the right of EG
            returnVal = CTLNestedStructure(CTLOperators.EG)     #Generate EG operator
            returnVal.addNestedOp(arg1,None)                    #Add op that was found recursively
            return returnVal                                    #return EG structure that points to returned above object
        elif nextChar == 'X':
            arg1 = generateNS(CTLString[3:len(CTLString) -1])                    #recursive call on everything to the right of EX
            returnVal = CTLNestedStructure(CTLOperators.EX)     #Generate EX operator
            returnVal.addNestedOp(arg1,None)                    #Add op that was found recursively
            return returnVal                                    #return EX structure that points to returned above object
        else:
            print "Invalid Formula"                             #Invalid if it gets here
            return                                              #returns to end generateNSion call
    elif CTLString[0] == '!':                                   #If we see a NOT operator
        arg1 = generateNS(CTLString[2:len(CTLString) - 1])     #recursive call on the rest of the string
        returnVal = CTLNestedStructure(CTLOperators.NOT)        #Generate Not operator
        returnVal.addNestedOp(arg1,None)                        #Add op that was found recursively
        return returnVal                                        #return not pointing to object that was return in above line
    elif CTLString[0] == '(':                                   #If we see an OR operator
        #######################################################################################################################
        #######################################################################################################################
        str1,str2 = returnOrStrings(CTLString)                  #first string is contained to left side of | to first (
        #######################################################################################################################
        #######################################################################################################################
        arg1 = generateNS(str1)                                 #recursive call for arg1
        arg2 = generateNS(str2)                                 #recursive call for arg2
        returnVal = CTLNestedStructure(CTLOperators.OR)         #Generate EU operator
        returnVal.addNestedOp(arg1,arg2)                        #Add ops that were found recursively
        return returnVal                                        #return EU w/ args that are the returned objects
    elif CTLString == 'p' or CTLString == 'q':                  #TERMINAL CASE
    #elif CTLString in returnApNames():                         #TERMINAL CASE
        returnVal = CTLNestedStructure(CTLOperators.AP)         #Create AP Op
        returnVal.addLabel(CTLString)                           #Add label
        return returnVal                                        #Return AP op
    else:
        print "Invalid Formula"

def returnOrStrings(string):
    '''
    Returns reference to list of two strings that OR operator operates on
    [start:end] => items start through end-1
    '''
    counterOpen = 1
    counterClosed = 0
    string = string[1:len(string)-1]#strip off outer parantheses
    for index,char in enumerate(string):
        if char == '(':
            counterOpen += 1
        if char == ')':
            counterClosed += 1
        elif char == '|':
            if counterOpen == counterClosed:
                return [string[:index-1],string[index+2:len(string)]]

def returnUntilStrings(string):
    '''
    Returns reference to list of two strings that EU operator operates on
    [start:end] => items start through end-1
    '''
    counterOpen = 1
    counterClosed = 0
    string = string[2:len(string)-1]#strip off outer parantheses and beginning E
    for index,char in enumerate(string):
        if char == '(':
            counterOpen += 1
        if char == ')':
            counterClosed += 1
        elif char == 'U':
            if counterOpen == counterClosed:
                return [string[:index-1],string[index+2:len(string)]]

if __name__ == "__main__":
    topOp = generateNS('!EG(EX(p|q)|E(pUq))')
    print topOp.getCTLFormulaString()
