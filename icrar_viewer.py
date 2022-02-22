import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QIcon

from casacore.tables import table as Table
from listmodel.casacore_list_model import CasacoreItemModel
from mainwindow.mainwindow_view import MainWindow
from tablemodel.casacore_table_model import CasacoreTableModel

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    window.viewmodel.listmodel = CasacoreItemModel(
        window.centralWidget(),
        []
    )

    if len(sys.argv) == 2:
        table = Table(sys.argv[1], ack=False)
        window.viewmodel.listmodel.append(table)
        window.viewmodel.tablemodel = CasacoreTableModel(
            window.centralWidget(),
            table
        )
    window.queryedit.setText("SELECT * FROM $t LIMIT 10000")
    window.queryedit.editingFinished.emit()

    window.centralWidget().show()
    sys.exit(app.exec())
