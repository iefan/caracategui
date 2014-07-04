#!/usr/bin/env python

# from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QKeySequence, QAction, QIcon, QMainWindow, QApplication, QWidget, QSizePolicy, QLabel, QFrame
from PyQt4.QtGui import QVBoxLayout, qApp, QActionGroup, QMessageBox, QStandardItemModel, QTableView, QTableWidgetItem, QDialogButtonBox
from PyQt4.QtGui import QPushButton, QStandardItem, QMenu, QItemDelegate, QStyleOptionComboBox, QComboBox, QAbstractItemView
from PyQt4.QtCore import SIGNAL, Qt, QVariant, QPyNullVariant
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

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
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # print(1)

        widget = QWidget()
        self.setCentralWidget(widget)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("caracate.db")
        if not self.db.open():
            QMessageBox.warning(None, "Phone Log",  "Database Error: %s" % db.lastError().text())
            sys.exit(1)

        headers = ["单位编码", "单位名称", "单位类别", "姓名"]

        self.userView = QTableView()
        self.userModel = QSqlTableModel(self.userView)
        self.userModel.setTable("user")
        self.userModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # self.userModel.setQuery(QSqlQuery("select unitsn, unitname, unitclass, unitpp from user"))
        self.userModel.select()
        # self.userModel.removeColumn(2)
        # self.userModel.removeColumn(0)
        self.userModel.setHeaderData(1, Qt.Horizontal, "单位编码")
        self.userModel.setHeaderData(3, Qt.Horizontal, "单位名称")
        self.userModel.setHeaderData(4, Qt.Horizontal, "单位类别")
        self.userModel.setHeaderData(5, Qt.Horizontal, "姓名")

        # self.userModel = QStandardItemModel(0, 0, self.userView)
        # self.userModel.setHorizontalHeaderLabels(headers)
        self.userView.setModel(self.userModel)
        self.userView.setColumnHidden(0, True) # hide sn
        self.userView.setColumnHidden(2, True) # hide password
        # print(2)
        combodelegate = ComboBoxDelegate(self, ["市残联", "金平区残联", "龙湖区残联", "濠江区残联"])
        # print(3)
        self.userView.setItemDelegateForColumn(3, combodelegate)
        self.userView.setStyleSheet("QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        # self.userView.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.userView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.userView.horizontalHeader().setStyleSheet("color: red");
        # self.userView.verticalHeader().hide()
        self.userView.verticalHeader().setFixedWidth(30)
        self.userView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.userView.setStyleSheet("font-size:14px; ");
        # print(4)
        # self.userView.show()

        # topFiller = QTableWidget()
        # topFiller.clear()
        # topFiller.setSortingEnabled(False)
        # topFiller.setRowCount(10)
        # topFiller.setColumnCount(len(headers))
        # topFiller.setHorizontalHeaderLabels(headers)
        # topFiller.setItem(1, 1, QTableWidgetItem("1"))
        # topFiller.resizeColumnsToContents()

        # topFiller = QWidget()
        self.userView.setSizePolicy(QSizePolicy.Expanding,
                QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        newusrbtn       = QPushButton("新增")
        modifypwdbtn    = QPushButton("修改密码")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        btnbox.addButton(newusrbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(modifypwdbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);

        self.infoLabel = QLabel(
                "<i>Choose a menu option, or right-click to invoke a context menu</i>",
                alignment=Qt.AlignCenter)
        self.infoLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        # bottomFiller = QWidget()
        # bottomFiller.setSizePolicy(QSizePolicy.Expanding,
        #         QSizePolicy.Expanding)

        vbox = QVBoxLayout()
        vbox.setMargin(5)
        vbox.addWidget(self.userView)
        vbox.addWidget(btnbox)
        vbox.addWidget(self.infoLabel)
        widget.setLayout(vbox)

        self.createActions()
        self.createMenus()

        message = "A context menu is available by right-clicking"
        self.statusBar().showMessage(message)

        savebtn.clicked.connect(self.saveUser)
        newusrbtn.clicked.connect(self.newUser)
        revertbtn.clicked.connect(self.revertUser)
        removebtn.clicked.connect(self.removeUser)
        # self.userView.clicked.connect(self.tableClick)
        # self.connect(savebtn, SIGNAL('clicked()'), self.saveUser)

        
        # self.createDb()
        # self.userView.show()

        self.setWindowTitle("结算系统")
        self.setMinimumSize(480,320)
        self.resize(720,600)

    def createDb(self):
        query = QSqlQuery()
        query.exec_("""CREATE TABLE user ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            unitsn      VARCHAR(40) NOT NULL,
            passwd      VARCHAR(40) NOT NULL,
            unitname    VARCHAR(40) NOT NULL,
            unitclass   VARCHAR(40) NOT NULL,
            unitpp      VARCHAR(40) NOT NULL)""")
        # query.exec_("insert into user values(101, 'aa', 'bb', 'cc', 'dd', 'ee')")
        query.exec_("select * from user")
        while query.next():
            print(query.value(0), query.value(1), query.value(2))
            # starttime DATETIME NOT NULL,
        # print("createdb")

    def removeUser(self):
        index = self.userView.currentIndex()
        row = index.row()
        print(index.isValid(), index.row())
        nameid = self.userModel.data(self.userModel.index(row, 0))
        # self.userModel.setFilter("id = 10");
        # self.userModel.select();
        # if self.userModel.rowCount() == 1:
        #     model.removeRows(0,1) // 如果要删除所有满足条件的记录则把1改成model.rowCount()
        #     model.submitAll();

        self.userModel.removeRows(row, 1)
        self.userModel.submitAll()
        self.userModel.database().commit()
        print("nameid")
        

    def revertUser(self):
        self.userModel.revertAll()
        self.userModel.database().rollback()

    def newUser(self):
        row = self.userModel.rowCount()
        self.userModel.insertRow(row)
        self.userModel.setData(self.userModel.index(row, 2), "123456") #set default password

    def saveUser(self):
        self.userModel.database().transaction()
        if self.userModel.submitAll():
            self.userModel.database().commit()
            print("save success!  ->commit")
        else:
            self.userModel.revertAll()
            self.userModel.database().rollback()
            print("save fail!  ->rollback")
        # model->database().transaction();
        # tmpitem = QStandardItem("张三")
        # self.userModel.setItem(0, 0, tmpitem)
        # print(self.userModel.database())
        # print("saveUser")

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.addAction(self.cutAct)
        menu.addAction(self.copyAct)
        menu.addAction(self.pasteAct)
        menu.exec_(event.globalPos())

    def newFile(self):
        self.infoLabel.setText("Invoked <b>File|New</b>")

    def open(self):
        self.infoLabel.setText("Invoked <b>File|Open</b>")
        	
    def save(self):
        self.infoLabel.setText("Invoked <b>File|Save</b>")

    def print_(self):
        self.infoLabel.setText("Invoked <b>File|Print</b>")

    def undo(self):
        self.infoLabel.setText("Invoked <b>Edit|Undo</b>")

    def redo(self):
        self.infoLabel.setText("Invoked <b>Edit|Redo</b>")

    def cut(self):
        self.infoLabel.setText("Invoked <b>Edit|Cut</b>")

    def copy(self):
        self.infoLabel.setText("Invoked <b>Edit|Copy</b>")

    def paste(self):
        self.infoLabel.setText("Invoked <b>Edit|Paste</b>")

    def bold(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Bold</b>")

    def italic(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Italic</b>")

    def leftAlign(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Left Align</b>")

    def rightAlign(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Right Align</b>")

    def justify(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Justify</b>")

    def center(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Center</b>")

    def setLineSpacing(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Set Line Spacing</b>")

    def setParagraphSpacing(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Set Paragraph Spacing</b>")

    def about(self):
        self.infoLabel.setText("Invoked <b>Help|About</b>")
        QMessageBox.about(self, "About Menu",
                "The <b>Menu</b> example shows how to create menu-bar menus "
                "and context menus.")

    def aboutQt(self):
        self.infoLabel.setText("Invoked <b>Help|About Qt</b>")


    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def createActions(self):
        self.newAct     = self.createAction("新建(&N)", self.newFile,   QKeySequence.New, "", "创建一个新的用户")
        self.openAct    = self.createAction("&Open...", self.open,   QKeySequence.Open, "", "Open an existing file")
        self.saveAct    = self.createAction("&Save", self.save,   QKeySequence.Save, "", "Save the document to disk")
        self.printAct   = self.createAction("&Print...", self.print_,   QKeySequence.Print, "", "Print the document")
        self.exitAct    = self.createAction("E&xit", self.close,   "Ctrl+Q", "", "Exit the application")
        self.undoAct    = self.createAction("&Undo", self.undo,   QKeySequence.Undo, "", "Undo the last operation")
        self.redoAct    = self.createAction("&Redo", self.redo,   QKeySequence.Redo, "", "Redo the last operation")
        self.cutAct     = self.createAction("Cu&t", self.cut,   QKeySequence.Cut, "", "Cut the current selection's contents to the clipboard")
        self.copyAct    = self.createAction("&Copy", self.copy,   QKeySequence.Copy, "", "Copy the current selection's contents to the clipboard")
        self.pasteAct   = self.createAction("&Paste", self.paste,   QKeySequence.Paste, "", "Paste the clipboard's contents")
        
        self.boldAct    = self.createAction("&Bold", self.bold,   "Ctrl+B", "", "Make the text bold", True)
        boldFont = self.boldAct.font()
        boldFont.setBold(True)
        self.boldAct.setFont(boldFont)

        self.italicAct  = self.createAction("&Italic", self.italic,   "Ctrl+I", "", "Make the text italic", True)
        italicFont = self.italicAct.font()
        italicFont.setItalic(True)
        self.italicAct.setFont(italicFont)

        self.setLineSpacingAct      = self.createAction("Set &Line Spacing...", self.setLineSpacing,   "", "", "Change the gap...")
        self.setParagraphSpacingAct = self.createAction("Set &Paragraph Spacing...", self.setParagraphSpacing,   "", "", "Change the gap between paragraphs")
        self.aboutAct   = self.createAction("&About", self.about,   "", "", "Show the application's About box")
        self.aboutQtAct = self.createAction("About &Qt", self.aboutQt,   "", "", "Show the Qt library's About box")
        self.aboutQtAct.triggered.connect(qApp.aboutQt)
  
        self.leftAlignAct  = self.createAction("&Left Align", self.leftAlign,  "Ctrl+L", "", "Left align the selected text", True)
        self.rightAlignAct = self.createAction("&Right Align", self.rightAlign,  "Ctrl+R", "", "Right align the selected text", True)
        self.justifyAct = self.createAction("&Justify", self.justify,  "Ctrl+J", "", "Justify the selected text", True)
        self.centerAct  = self.createAction("&Center", self.center,  "Ctrl+C", "", "Center the selected text", True)

        self.alignmentGroup = QActionGroup(self)
        self.alignmentGroup.addAction(self.leftAlignAct)
        self.alignmentGroup.addAction(self.rightAlignAct)
        self.alignmentGroup.addAction(self.justifyAct)
        self.alignmentGroup.addAction(self.centerAct)
        self.leftAlignAct.setChecked(True)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.formatMenu = self.editMenu.addMenu("&Format")
        self.formatMenu.addAction(self.boldAct)
        self.formatMenu.addAction(self.italicAct)
        self.formatMenu.addSeparator().setText("Alignment")
        self.formatMenu.addAction(self.leftAlignAct)
        self.formatMenu.addAction(self.rightAlignAct)
        self.formatMenu.addAction(self.justifyAct)
        self.formatMenu.addAction(self.centerAct)
        self.formatMenu.addSeparator()
        self.formatMenu.addAction(self.setLineSpacingAct)
        self.formatMenu.addAction(self.setParagraphSpacingAct)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
