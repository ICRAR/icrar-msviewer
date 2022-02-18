
from PySide6.QtCore import (
    QObject, QFile, QAbstractTableModel,
    Qt, QCoreApplication, Signal,
    QModelIndex, QPersistentModelIndex, SIGNAL,
    Slot
)
from casacore.tables import taql
from tablemodel.casacore_table_model import CasacoreTableModel

class MainWindowViewModel(QObject):
    """doc"""
    _tablemodel: QAbstractTableModel | None
    on_model_set = Signal()

    @property
    def tablemodel(self):
        """doc"""
        return self._tablemodel

    @tablemodel.setter
    def tablemodel(self, value):
        self._tablemodel = value
        self.on_model_set.emit()

    def execute_query(self, query: str):
        """doc"""
        if isinstance(self.tablemodel, CasacoreTableModel):
            t = self.tablemodel.table
            # NOTE: query resolves interpreter variables with $, e.g. $t
            self.tablemodel.querytable = taql(query, tables=[t])

    def open_table(self):
        """doc"""
        pass

    def save_table(self):
        """doc"""
        pass

    def toggle_show_index(self):
        """doc"""
        pass
