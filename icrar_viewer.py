import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QIcon

from casacore.tables import table as Table
from mainwindow.mainwindow_view import MainWindow
from tablemodel.casacore_table_model import CasacoreTableModel

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    window.viewmodel.tablemodel = CasacoreTableModel(
        window.centralWidget(),
        Table("/home/callan/Code/icrar/msdata/ska/AA05LOW.ms/", ack=False)
    )
    window.queryedit.setText("select * from $t LIMIT 10000")
    window.viewmodel.execute_query(window.queryedit.text())

    window.centralWidget().show()
    sys.exit(app.exec())
