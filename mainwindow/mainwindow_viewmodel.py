
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView,
    QLineEdit, QSplitter, QFileDialog,
    QStatusBar, QProgressBar, QToolTip,
    QTabWidget, QWidget
)
from PySide6.QtCore import (
    QObject, QFile, QAbstractTableModel,
    Qt, QCoreApplication, Signal,
    QModelIndex, QPersistentModelIndex, SIGNAL,
    Slot
)
from casacore.tables import table as Table
from casacore.tables import taql
from tablemodel.casacore_table_model import CasacoreTableModel

class MainWindowViewModel(QObject):
    """doc"""
    _taqlquery: str = ""
    _selected_tablemodel: QAbstractTableModel | None

    on_model_set = Signal() # table is changed by updating selected tablemodel

    @property
    def tablemodel(self):
        """doc"""
        return self._selected_tablemodel

    @tablemodel.setter
    def tablemodel(self, value):
        self._selected_tablemodel = value
        self.on_model_set.emit()

    @property
    def taqlquery(self):
        """the completed taql query ready for execution"""
        return self._taqlquery

    @taqlquery.setter
    def taqlquery(self, value):
        self._taqlquery = value
        self._execute_query()

    def _execute_query(self):
        """doc"""
        if isinstance(self.tablemodel, CasacoreTableModel):
            t = self.tablemodel.table
            # NOTE: query resolves interpreter variables with $, e.g. $t
            self.tablemodel.querytable = taql(self._taqlquery, tables=[t])

    def load_ms(self, ms_path):
        """doc"""
        # TODO: alternatively treat this is a ModelView and only
        # update the internal table
        self.tablemodel = CasacoreTableModel(
            None,
            Table(ms_path, ack=False)
        )

    @Slot()
    def toggle_show_index(self):
        """doc"""
        #self.table
