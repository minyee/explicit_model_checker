#from tkinter import Tk, Label, Button, W, E, Entry, StringVar
# for Python2
from Tkinter import *  ## notice capitalized T in Tkinter
import tkFileDialog
from vhdlParser import *
from ctl_ops import *
from recursiveNS import *

#from Tkinter import *from Tkinter import *
#from Tkinter import Entry

class GUI:
    '''
    Create GUI class from tkinter.
    Potential issues:
        => Need to make sure you can't keep opening new AP/CTL editor windows once one is opening
        => Need to make sure that the clearCTL command actually destroys all of the CTLNestedStructure objects
    '''
    def __init__(self):
        '''
        how to pass value to function
        Need to display PD's values
        Need to display voltage values
        '''

        #GUI STUFF
        self.root = Tk()
        self.KS = None
        self.NS = None
        self.root.title("VHDL CTL Explicit State Model Checker")
        self.dispVHDLPrompt()

    def dispVHDLPrompt(self):
        '''
        Prompts user to select vhdl file
        '''
        #VHDL File entry
        self.selectFileButton = Button(self.root, text="Select FSM File", command=lambda: self.selectFile())
        self.genKSButton = Button(self.root, text="Generate Kripke Structure", command=lambda: self.generateKripkeStructure())
        self.VHDLFilename = StringVar()
        self.VHDLFileEntry = Entry(self.root, textvariable=self.VHDLFilename)
        self.selectFileButton.grid(row=0,column=0)
        self.VHDLFileEntry.grid(row=0,column=1)
        self.genKSButton.grid(row=0,column=2)
        self.root.mainloop()

    def selectFile(self):
        self.VHDLFilename.set(tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("fsm files","*.vhd"),("all files","*.*"))))

    def generateKripkeStructure(self):
        #DESTROY OLD KS IF IT EXISTS
        f = self.VHDLFileEntry.get()
        if '.vhd' in f:
            self.parser = vhdlParser(f)                      #Instantiates parser
            self.parser.parseVHDL()                          #Generates .krip file
            self.KS = self.parser.returnKripkeStructure()   #creates data structure from .krip file
            self.openKSEditor()                         #Opens KS editor using data structure
        elif '.krip' in f:
            self.parser = vhdlParser(f)                      #Instantiates parser
            self.KS = self.parser.returnKripkeStructure()   #creates data structure from .krip file
            self.openKSEditor()                         #Opens KS editor using data structure
        else:
            print "Incompatible file type. Please try again."

    def openKSEditor(self):
        '''
        Opens second window to modify and evaluate KS
        '''
        #self.KSEditor.destroy() #CLOSE OLD KSEditor
        outputs = []
        self.CTLEquation = StringVar()
        self.CTLEquation.set('')
        self.KSEditor = Toplevel(self.root)
        self.KSEditor.title(self.parser.filename)
        # create all of the main containers
        self.KSEditor.APEditFrame = Frame(self.KSEditor, width=450, height=200)
        self.KSEditor.CTLEditFrame = Frame(self.KSEditor, width=450, height=50)
        self.KSEditor.APEditFrame.grid(row=0,column=0)
        self.KSEditor.CTLEditFrame.grid(row=1,column=0)
        #output option menu
        for key in self.KS.OutputDictOfDict[0]:
            outputs.append(key)
        self.KSEditor.outputLabel = Label(self.KSEditor.APEditFrame,text='Output')
        self.KSEditor.outputVar = StringVar()
        self.KSEditor.outputVar.set(outputs[0]) # initial value
        self.KSEditor.optionOutput = OptionMenu(self.KSEditor.APEditFrame, self.KSEditor.outputVar, *outputs)
        #AP EDITOR######################################################################################################
        conditionalOperators = ["==",">","<"]
        self.KSEditor.APEditorLabel = Label(self.KSEditor.APEditFrame,text='Atomic Proposition Editor',font = "Helvetica 16 bold")
        self.KSEditor.COPLabel = Label(self.KSEditor.APEditFrame,text='Conditional Operator')
        self.KSEditor.COPVar = StringVar()
        self.KSEditor.COPVar.set(conditionalOperators[0]) # initial value
        self.KSEditor.optionCOP = OptionMenu(self.KSEditor.APEditFrame, self.KSEditor.COPVar, *conditionalOperators)
        self.KSEditor.ValueLabel = Label(self.KSEditor.APEditFrame,text='Binary Value')
        self.KSEditor.Value = StringVar()
        self.KSEditor.ValueEntry = Entry(self.KSEditor.APEditFrame, textvariable=self.KSEditor.Value)
        self.KSEditor.generateAPButton = Button(self.KSEditor.APEditFrame, text="Add AP", command=lambda: self.generateAP())
        self.KSEditor.APNameLabel = Label(self.KSEditor.APEditFrame,text='AP Label')
        self.KSEditor.APNameVal = StringVar()
        self.KSEditor.APNameEntry = Entry(self.KSEditor.APEditFrame, textvariable=self.KSEditor.APNameVal)
        self.KSEditor.printAPsButton = Button(self.KSEditor.APEditFrame, text="Print APs", command=lambda: self.printAPs())
        self.KSEditor.clearAPsButton = Button(self.KSEditor.APEditFrame, text="Clear APs", command=lambda: self.clearAPs())
        #GRID PLACEMENT
        self.KSEditor.APEditorLabel.grid(row=0,column=0,columnspan=6)
        self.KSEditor.outputLabel.grid(row = 1, column =0)
        self.KSEditor.optionOutput.grid(row = 1, column =1)
        self.KSEditor.COPLabel.grid(row = 1, column =2)
        self.KSEditor.optionCOP.grid(row = 1, column =3)
        self.KSEditor.ValueLabel.grid(row = 1, column =4)
        self.KSEditor.ValueEntry.grid(row = 1, column =5)
        self.KSEditor.APNameLabel.grid(row = 2, column =0)
        self.KSEditor.APNameEntry.grid(row = 2, column =1)
        self.KSEditor.generateAPButton.grid(row = 2, column =2)
        self.KSEditor.clearAPsButton.grid(row = 2, column =3)
        self.KSEditor.printAPsButton.grid(row = 2, column =4)

        ######################################################################################################
        self.KSEditor.CTLEditorLabel = Label(self.KSEditor.APEditFrame,text='CTL Equation Editor',font = "Helvetica 16 bold")
        self.KSEditor.CTLEntry = Entry(self.KSEditor.CTLEditFrame, textvariable=self.CTLEquation)
        self.selectedAP = StringVar()
        self.selectedAP.set('')
        self.KSEditor.enterAP = Button(self.KSEditor.CTLEditFrame, text="Input AP", command=lambda: self.addAp(self.selectedAP.get()))
        self.KSEditor.optionAPs = OptionMenu(self.KSEditor.CTLEditFrame, self.selectedAP, *self.returnApNames())
        self.KSEditor.enterCTL = Button(self.KSEditor.CTLEditFrame, text="Enter", command=lambda: self.generateNestedStructure())
        self.KSEditor.clearCTL = Button(self.KSEditor.CTLEditFrame, text="Clear CTL", command=lambda: self.clearCTL())
        self.KSEditor.CTLDisplay = Label(self.KSEditor.CTLEditFrame,bg='white',text=self.CTLEquation)
        self.KSEditor.CTLEditorLabel.grid(row = 3,column=0,columnspan=6)
        self.KSEditor.optionAPs.grid(row = 0,column=0,sticky=E+W+N+S)
        self.KSEditor.enterAP.grid(row = 0,column=1,sticky=E+W+N+S)
        self.KSEditor.CTLEntry.grid(row = 1, column = 0,sticky=E+W+N+S)
        self.KSEditor.enterCTL.grid(row = 1, column = 1,sticky=E+W+N+S)
        self.KSEditor.clearCTL.grid(row = 2, column = 0,sticky=E+W+N+S)

    def generateNestedStructure(self):
        '''
        Generates nested structure from the input CTL formula
        '''
        self.NS = generateNS(self.CTLEquation.get())
        print self.NS.getCTLFormulaString()
        #print self.NS.getCTLFormulaString()

    def updateDropdown(self):
        names = self.returnApNames()
        menu = self.KSEditor.optionAPs['menu']
        menu.delete(0,'end')
        for name in names:
            menu.add_command(label=name, command=lambda selectedName=name: self.selectedAP.set(selectedName))

    def clearCTL(self):
        self.CTLEquation.set('')
        self.NS = None
        #self.KSEditor.CTLDisplay.configure(text=self.CTLEquation)

    def returnApNames(self):
        ApNames = []
        if self.KS.ApList :
            for name in self.KS.ApList:
                ApNames.append(name[3])
            return ApNames
        else:
            return ['','']

    def addAp(self,Ap):
        self.CTLEquation.set(self.CTLEquation.get()+Ap)

    def generateAP(self):
        '''
        generates AP and modifies kripke structure
        '''

        outputVal = str(self.KSEditor.Value.get())
        conditionalOperator = str(self.KSEditor.COPVar.get())
        ApName = str(self.KSEditor.APNameVal.get()).lower()
        outputName = str(self.KSEditor.outputVar.get())

        if re.match('^[a-zA-Z]+$',ApName) is None:
            print "Invalid AP name. Please use only uppercase and lowercase letters."
            return
        try:
            decnum = int(outputVal)
            for item in self.KS.ApList:
                if item[0] == outputName:
                    print "AP Ignored: only one AP may exist per output"
                    return
                elif item[3] == ApName:
                    print "AP Ignored: must have unique AP labels"
                    return
            if self.KS.addAP([outputName,conditionalOperator,outputVal,ApName]):
                print ApName + ': ' + outputName + conditionalOperator + outputVal
            else:
                print "Error Adding Atomic Proposition"
        except ValueError:
            print "Enter a number! Please try again.\n"
        self.updateDropdown()

    def printAPs(self):
        '''
        prints all APs attached to KS and values for each node
        '''
        print "\nList of APs => "
        for item in self.KS.ApList:
            print '\t' + item[3] + ': ' + item[0] + ' ' + item[1] + ' ' + item[2]

    def clearAPs(self):
        '''
        Clears all APs from KS and Nodes
        '''
        self.KS.ApDictOfDict = {}
        self.KS.ApList = []
        self.updateDropdown()
        self.selectedAP.set('')
        for node in self.KS.graphNodeList:
            node.ApDict = {}

if __name__ == "__main__":
    my_gui = GUI()
    #GUIparseCTL("")
