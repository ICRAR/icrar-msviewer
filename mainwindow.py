# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
from typing import Any
import sys
from overrides import overrides
from events import Events

from PySide6.QtWidgets import QApplication, QMainWindow, QTableView
from PySide6.QtCore import QFile, QAbstractTableModel, Qt, QCoreApplication, QModelIndex, QPersistentModelIndex, SIGNAL
from PySide6.QtUiTools import QUiLoader

from pandas import DataFrame
from casacore.tables import table as Table

from casacore_table_model import CasacoreTableModel
from pandas_table_model import PandasTableModel


class ViewModelEvents(Events):
    """doc"""
    __events__ = ('on_model_set')

class MainWindowModel:
    """doc"""
    _table: Table | None


class MainWindowViewModel:
    """doc"""
    _tablemodel: QAbstractTableModel | None
    events = ViewModelEvents()

    @property
    def tablemodel(self):
        return self._tablemodel

    @tablemodel.setter
    def tablemodel(self, value):
        self._tablemodel = value
        self.events.on_model_set()

    def __init__(self):
        pass

    def open_table(self):
        pass

    def save_table(self):
        pass

    def toggle_show_index(self):
        pass


class MainWindow(QMainWindow):
    """
    Main window component of icrar casacore explorer.
    Current primary responsibility is displaying table view.
    Binding to viewmodels is performed via code.
    Views contain the app heirarchy/backbone.
    Views always own a single viewmodel context.
    """
    _viewmodel = MainWindowViewModel()

    def __init__(self):
        super().__init__()
        self.load_ui()

    @property
    def viewmodel(self):
        """Returns the viewmodel"""
        return self._viewmodel

    def load_ui(self):
        """_summary_
        """
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        self.tableview = self.findChild(QTableView)
        self.tableview.setSortingEnabled(True)

        # bindings
        # Since Qt XML has binding not have binding syntax, if the model gets reassigned
        # then child view components should fetch the model.
        self.viewmodel.events.on_model_set += lambda: self.tableview.setModel(self.viewmodel.tablemodel)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = MainWindow()

    # load models via code
    tabledataframe =  DataFrame({
        'id': [3,2,1],
        'name': ['a', 'b', 'c'],
        'age': [23,65,42]
    })
    widget.viewmodel.tablemodel = PandasTableModel(
        widget,
        tabledataframe
    )
    # widget.viewmodel.tablemodel = CasacoreTableModel(
    #     widget,
    #     Table("/home/callan/Code/icrar/msdata/ska/AA05LOW.ms/")
    # )

    widget.centralWidget().show()
    sys.exit(app.exec())
