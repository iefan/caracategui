from PyQt4.QtGui import  QItemDelegate, QComboBox
from PyQt4.QtCore import QPyNullVariant, Qt

class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent, itemslist=["a", "b", "c"]):
        QItemDelegate.__init__(self, parent)
        # itemslist = ["a", "b", "c"]
        self.itemslist = itemslist
        self.parent = parent

    # def paint(self, painter, option, index):        
    #     # Get Item Data
    #     value = index.data(Qt.DisplayRole).toInt()[0]
    #     # value = self.itemslist[index.data(QtCore.Qt.DisplayRole).toInt()[0]]
    #     # fill style options with item data
    #     style = QApplication.style()
    #     opt = QStyleOptionComboBox()
    #     opt.currentText = str(self.itemslist[value])
    #     opt.rect = option.rect


    #     # draw item data as ComboBox
    #     style.drawComplexControl(QStyle.CC_ComboBox, opt, painter)
    #     self.parent.openPersistentEditor(index)

    def createEditor(self, parent, option, index):

        ##get the "check" value of the row
        # for row in range(self.parent.model.rowCount(self.parent)):
            # print row

        self.editor = QComboBox(parent)
        self.editor.addItems(self.itemslist)
        self.editor.setCurrentIndex(0)
        self.editor.installEventFilter(self)    
        # self.connect(self.editor, SIGNAL("currentIndexChanged(int)"), self.editorChanged)

        return self.editor

    # def setEditorData(self, editor, index):
        # value = index.data(QtCore.Qt.DisplayRole).toInt()[0]
        # editor.setCurrentIndex(value)

    def setEditorData(self, editor, index): 
        curtxt = index.data(Qt.DisplayRole)
        # print(type(curtxt)== QPyNullVariant )
        if type(curtxt) == type(1):
            curindx = int(index.data(Qt.DisplayRole))
            curtxt = self.itemslist[curindx]
        elif type(curtxt)== QPyNullVariant:
            curtxt = ""
        pos = self.editor.findText(curtxt)
        if pos == -1:  
            pos = 0
        self.editor.setCurrentIndex(pos)


    def setModelData(self,editor,model,index):
        curindx = self.editor.currentIndex()
        text = self.itemslist[curindx]
        model.setData(index, text)


    def updateEditorGeometry(self, editor, option, index):
        self.editor.setGeometry(option.rect)

    def editorChanged(self, index):
        check = self.editor.itemText(index)
        id_seq = self.parent.selectedIndexes[0][0]
        update.updateCheckSeq(self.parent.db, id_seq, check)
        