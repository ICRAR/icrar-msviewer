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
from typing import List
from casacore.tables import table as Table
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, SIGNAL

from icrar.mainwindow.mainwindow_model import MainWindowModel

class MSTableViewModel(QAbstractTableModel):
    """
    https://stackoverflow.com/questions/19411101/pyside-qtableview-example
    """
    _model: MainWindowModel

    def __init__(self, parent, model: MainWindowModel):
        """doc"""
        super().__init__(parent)
        self._model = model

        # cache
        if self.querytable:
            self._queryrownumbers = self.querytable.rownumbers()

        # Experimental
        self._showindex = True

    @property
    def tables(self):
        """doc"""
        return self._model.selected_tables

    @property
    def querytable(self) -> Table | None:
        """doc"""
        return self._model.query_table


    def handle_layoutAboutToBeChanged(self):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

    def handle_layoutChanged(self):
        if self.querytable:
            self._queryrownumbers = self.querytable.rownumbers()
        self.emit(SIGNAL("layoutChanged()"))

    # @overrides
    def rowCount(self, parent) -> int:
        """doc"""
        return self.querytable.nrows() if self.querytable else 0

    # @overrides
    def columnCount(self, parent) -> int:
        """doc"""
        if not self.querytable:
            return 0
        return self.querytable.ncols() + 1 if self._showindex else self.querytable.ncols()

    # @overrides
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> str | None:
        """doc"""
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        if not self.querytable:
            return None
        if not self._showindex:
            return str(self.querytable[index.row()][self.querytable.colnames()[index.column()]])
        else:
            start = time.time()
            if index.column() == 0:
                res = str(self._queryrownumbers[index.row()])
            else:
                res = str(self.querytable[index.row()][self.querytable.colnames()[index.column()-1]])
            end = time.time()
            #print(f"data[{index.row()},{index.column()}] , {end-start}")
            return res

    # @overrides
    def headerData(self, col, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """doc"""
        if self.querytable and orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if not self._showindex:
                return self.querytable.colnames()[col]
            else:
                return 'index' if col == 0 else self.querytable.colnames()[col-1]
        return None

    # @overrides
    def sort(self, col: int, order: Qt.SortOrder):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        #self.df.sort_values(by=self.df.columns[col], inplace=True, ascending=(order == Qt.AscendingOrder))
        self.emit(SIGNAL("layoutChanged()"))

    # @overrides
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """docs"""
        default = Qt.ItemNeverHasChildren | Qt.ItemIsEnabled # | Qt.ItemIsSelectable | Qt.ItemIsEditable
        if not self._showindex:
            return default
        else:
            return default if index.column() > 0 else Qt.ItemNeverHasChildren

    # @overrides
    def setData(self, index, value, role: Qt.ItemDataRole):
        """docs"""
        return False
        # datatype = self.df[self.df.columns[index.column()]].dtype
        # try:
        #     self.df.iloc[index.row(), index.column()] = datatype.type(value)
        #     return True
        # except ValueError:
        #     return False
