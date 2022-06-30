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
import time
from PySide6.QtCore import QObject, Signal, Slot
from casacore.tables import table as Table
from casacore.tables import taql
from icrar.listmodel.ms_list_model import MSListModel
from icrar.mainwindow.mainwindow_model import MainWindowModel
from icrar.mainwindow.msinfo.msinfo_viewmodel import MSInfoViewModel
from icrar.tablemodel.ms_table_model import MSTableModel


class MainWindowViewModel(QObject):
    """doc"""
    _model: MainWindowModel
    _list_viewmodel: MSListModel
    _selected_table_viewmodel: MSTableModel | None = None
    _info_viewmodel: MSInfoViewModel | None = None

    # TODO: only publicly expose connect and disconnect

    on_status_message = Signal(str, int)
    on_list_model_set = Signal(MSListModel) # opened ms list
    # NOTE: table is changed by updating selected tablemodel
    on_table_model_set = Signal() # selected ms table

    def __init__(self, parent: QObject, model: MainWindowModel):
        super().__init__(parent)
        self._model = model
        self._list_viewmodel = MSListModel(parent, [])

    @property
    def listmodel(self):
        """doc"""
        return self._list_viewmodel

    @listmodel.setter
    def listmodel(self, value):
        self._list_viewmodel = value
        self.on_list_model_set.emit(value)

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
        self._model.taqlquery = value
        self._execute_query()

    def load_ms(self, ms_path: str):
        """
        Loads a casacore table to the list of open ms
        """
        table = Table(ms_path, ack=False)
        self.listmodel.append(table)
        # TODO: alternatively treat this as a ModelView and only update the internal table
        self.tablemodel = MSTableModel(None, table)
        self._execute_query()
        self.on_status_message.emit(f"Opened MS {ms_path}", 3000)


    def select_ms(self, index: int):
        """
        Selects an already loaded measurement set
        """
        self.tablemodel = MSTableModel(None, self.listmodel.get(index))
        self._execute_query()
        self.on_status_message.emit(f"Selected MS {self.tablemodel.table.name()}", 3000)

    @Slot()
    def toggle_show_index(self):
        """doc"""
        #self.table

    def _execute_query(self):
        """
        Triggers the querying of the selected table using the current
        model query string.
        """
        if self._model.taqlquery and isinstance(self.tablemodel, MSTableModel):
            t = self.tablemodel.table
            # NOTE: query resolves interpreter variables with $, e.g. $t
            start = time.time()
            self.tablemodel.querytable = taql(
                self._model.taqlquery,
                tables=[t],
                locals={"":""}
            )
            end = time.time()
            time_ms = (end-start)*1000.0

            self.on_status_message.emit(
                f"Queried MS {self.tablemodel.table.name()} in {time_ms}ms",
                3000
            )
