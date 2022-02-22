#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia, 2021
#    Copyright by UWA (in the framework of the ICRAR)
#    All rights reserved
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from PySide6.QtCore import QObject, Signal, Slot
from casacore.tables import table as Table
from casacore.tables import taql
from listmodel.casacore_list_model import CasacoreListModel
from mainwindow.mainwindow_model import MainWindowModel
from tablemodel.casacore_table_model import CasacoreTableModel


class MainWindowViewModel(QObject):
    """doc"""
    _model: MainWindowModel
    _list_viewmodel: CasacoreListModel
    _selected_table_viewmodel: CasacoreTableModel | None = None

    # TODO: only publicly expose connect and disconnect

    on_status_message = Signal(str, int)
    on_list_model_set = Signal() # opened ms list
    # NOTE: table is changed by updating selected tablemodel
    on_table_model_set = Signal() # selected ms table

    def __init__(self, parent: QObject, model: MainWindowModel):
        super().__init__(parent)
        self._model = model
        self._list_viewmodel = CasacoreListModel(parent, [])

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
        """Loads a casacore table to the list of open ms"""
        table = Table(ms_path, ack=False)
        self.listmodel.append(table)
        # TODO: alternatively treat this as a ModelView and only update the internal table
        self.tablemodel = CasacoreTableModel(None, table)
        self.on_status_message.emit(f"Opened {ms_path}", 3000)


    def select_ms(self, index):
        """selects an already loaded ms"""
        self.tablemodel = CasacoreTableModel(None, self.listmodel.get(index))
        self.on_status_message.emit(f"Selected {self.listmodel.get(index).name()}", 3000)

    @Slot()
    def toggle_show_index(self):
        """doc"""
        #self.table
