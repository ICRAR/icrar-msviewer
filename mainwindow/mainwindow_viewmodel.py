
from PySide6.QtCore import (
    QObject, Signal, Slot
)
from casacore.tables import table as Table
from casacore.tables import taql
from listmodel.casacore_list_model import CasacoreItemModel
from mainwindow.mainwindow_model import MainWindowModel
from tablemodel.casacore_table_model import CasacoreTableModel

class MainWindowViewModel(QObject):
    """doc"""
    _model: MainWindowModel
    _list_viewmodel: CasacoreItemModel | None = None
    _selected_table_viewmodel: CasacoreTableModel | None = None

    # TODO: only publicly expose connect and disconnect

    on_list_model_set = Signal() # opened ms list
    # NOTE: table is changed by updating selected tablemodel
    on_table_model_set = Signal() # selected ms table

    def __init__(self, parent: QObject, model: MainWindowModel):
        super().__init__(parent)
        self._model = model

    @property
    def listmodel(self):
        """doc"""
        return self._list_viewmodel

    @listmodel.setter
    def listmodel(self, value):
        self._list_viewmodel = value
        self.on_list_model_set.emit()

    @property
    def tablemodel(self):
        """Selected Table ViewModel for a QTableView child"""
        return self._selected_table_viewmodel

    @tablemodel.setter
    def tablemodel(self, value):
        self._selected_table_viewmodel = value
        self.on_table_model_set.emit()

    @property
    def taqlquery(self):
        """the completed taql query ready for execution"""
        return self._model.taqlquery

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
        table = Table(ms_path, ack=False)
        self.listmodel.append(table)
        self.tablemodel = CasacoreTableModel(None, table)

    @Slot()
    def toggle_show_index(self):
        """doc"""
        #self.table
