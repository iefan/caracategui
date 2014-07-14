from PyQt4.QtGui import QDialog, QKeySequence, QAction, QIcon, QMainWindow, QApplication, QWidget, QSizePolicy, QLabel, QFrame, QTabWidget
from PyQt4.QtGui import QVBoxLayout, qApp, QActionGroup, QMessageBox, QStandardItemModel, QTableView, QTableWidgetItem, QDialogButtonBox
from PyQt4.QtGui import QPushButton, QStandardItem, QMenu, QItemDelegate, QStyleOptionComboBox, QComboBox, QAbstractItemView
from PyQt4.QtCore import SIGNAL, Qt, QVariant, QPyNullVariant
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

def globaldb():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("caracate.db")
    if not db.open():
        QMessageBox.warning(None, "Phone Log",  "Database Error: %s" % db.lastError().text())
        sys.exit(1)
    return db