import sys
from authorLib import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFrame, QCheckBox,QRadioButton, QLineEdit

class AuthorListDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AuthorListDialog, self).__init__()
        ccc = uic.loadUi("authorList.ui", self)
        self.setWindowTitle("Format Authors")
        #editFrame = self.findchil
        self.loadChildren()
        self.addEvents()
        self.authors = AuthorList()

        #for i in self.TextEdits:
            #i.setProperty("changeEvent", self.changeTex)
            #i.changeEvent = self.changeText
    def addEvents(self):
        self.SourceText.textChanged.connect(self.eventProcess)
        self.EnableSanitizer.stateChanged.connect(self.eventProcess)
        for i in self.LineEdits:
            i.textChanged.connect(self.eventProcess)
        for i in self.RadioButtons:
            i.toggled.connect(self.eventProcess)
        #self.FnLn.toggled.connect(self.eventProcess)

    def eventProcess(self):
        es = self.sender()
        esname = es.objectName()
        #print(es,esname)
        if esname == "SourceText" or esname == "FnLn":
            self.eventUpdate()
            return
        if es in self.SanitizerEdits:
            #print("eP->SE->checked:", self.EnableSanitizer.property("checked"))
            if self.EnableSanitizer.property("checked"):
                self.eventUpdate()
            return
        if es in self.AuthorEdits:
            self.eventUpdate()
    def eventUpdate(self):
        #print("updating...")
        if self.FnLn.property("checked") == False:
            order = "lnfn"
        else:
            order = "fnln"
        source = self.SourceText.property("plainText")
        if self.EnableSanitizer.property("checked"):
            g1 = self.G1Regex.property("text")
            g2 = self.G2Regex.property("text")
            sp = unescape(self.SpacingChar.property("text"))
            source = sanitize(source,sp,g1,g2)
            print("sanitized", source)
        entrysep = self.EntrySeparator.property("text")
        lnsep = self.FnLnSeparator.property("text")
        updText = ""
        try:
            self.authors = readAuthors(source, entrysep, order, lnsep)
            updText = str(self.authors)
        except:
            print("Regex Error in readAuthors(source, entrysep, order, lnsep):",source,entrysep,order,lnsep)
            updText = "Error in Regex"
        finally:
            self.OutputText.setProperty("plainText", str(self.authors))
        #print(entrysep, lnsep, str(self.authors))
        #print(sourceList)


    def loadChildren(self):
        self.FnLn = self.findChild(QRadioButton, "FnLn")
        self.LnFn = self.findChild(QRadioButton, "LnFn")
        self.FnLnSeparator = self.findChild(QLineEdit,"FnLnSeparator")
        self.EntrySeparator = self.findChild(QLineEdit, "EntrySeparator")
        self.SourceText = self.findChild(QPlainTextEdit, "SourceText")
        self.OutputText = self.findChild(QPlainTextEdit, "OutputText")

        self.EnableSanitizer = self.findChild(QCheckBox, "EnableSanitizer")
        self.G1Regex = self.findChild(QLineEdit, "G1Regex")
        self.G2Regex = self.findChild(QLineEdit, "G2Regex")
        self.SpacingChar = self.findChild(QLineEdit, "SpacingChar")

        self.CheckBoxes = (self.EnableSanitizer)
        self.LineEdits = (self.G1Regex, self.G2Regex, self.SpacingChar, self.FnLnSeparator, self.EntrySeparator)
        self.TextEdits = (self.SourceText, self.OutputText)
        self.RadioButtons = (self.FnLn, self.LnFn)
        self.SanitizerEdits = (self.G1Regex, self.G2Regex, self.SpacingChar)
        self.AuthorEdits = (self.FnLnSeparator, self.EntrySeparator)

    def loadAllChildren(self):
        children = self.children()
        optionsFrame = children[0]
        editFrame = children[1]
        for i in optionsFrame.children():
            self.__dict__[i.objectName()] = i
        for i in editFrame.children():
            self.__dict__[i.objectName()] = i
        #print(self.EnableSanitizer)
        #print(self.__dict__)
    #def updateText(self):
        #if self.EnableSanitizer

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    authorDialog = AuthorListDialog()
    authorDialog.show()
    sys.exit(app.exec_())
