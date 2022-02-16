# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from overrides import overrides

from PySide6.QtWidgets import QApplication, QMainWindow, QTableView
from PySide6.QtCore import QFile, QAbstractTableModel, Qt, QCoreApplication, QModelIndex, QPersistentModelIndex, SIGNAL
from PySide6.QtUiTools import QUiLoader

from pandas import DataFrame
from casacore.tables import table as Table

from casacore_table_model import CasacoreTableModel
from pandas_table_model import PandasTableModel

class MainWindow(QMainWindow):
    """
    Main window component of icrar casacore explorer.
    Current primary responsibility is displaying table view.
    Binding to viewmodels is performed via code.
    Views contain the app heirarchy/backbone.
    Views always own a single viewmodel context.
    """
    _tableviewmodel = None

    def __init__(self):
        super().__init__()
        self.load_ui()

    # TODO: move to viewmodel
    @property
    def tableviewmodel(self):
        """Returns the table model"""
        return self._tableviewmodel

    @tableviewmodel.setter
    def tableviewmodel(self, value):
        self._tableviewmodel = value
        self.tableview.setModel(self.tableviewmodel)

    def load_ui(self):
        """doc"""
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        # bindings
        self.tableview = self.findChild(QTableView)
        self.tableview.setModel(self.tableviewmodel)
        self.tableview.setSortingEnabled(True)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = MainWindow()

    # model
    # tabledataframe =  DataFrame({
    #     'id': [3,2,1],
    #     'name': ['a', 'b', 'c'],
    #     'age': [23,65,42]
    # })
    # self.tablemodel = PandasTableModel(
    #     self,
    #     self.tabledataframe)
    widget.tableviewmodel = CasacoreTableModel(
        widget,
        Table("/home/callan/Code/icrar/msdata/ska/AA05LOW.ms/")
    )

    widget.centralWidget().show()
    sys.exit(app.exec())
