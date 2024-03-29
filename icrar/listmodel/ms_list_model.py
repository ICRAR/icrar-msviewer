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
from typing import List
from casacore.tables import table as Table
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, SIGNAL

class MSListModel(QAbstractListModel):
    """Provides a viewmodel for a list of open casacore ms"""
    _list: List[Table]

    def __init__(self, parent: None, list: List[Table], *args):
        super().__init__(parent)
        self._list = list

    def append(self, item):
        """doc"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self._list.append(item)
        self.emit(SIGNAL("layoutChanged()"))

    def get(self, index):
        """doc"""
        return self._list[index]

    # @overrides
    def rowCount(self, parent: None) -> int:
        """
        Returns the number of rows under the given parent.
        When the parent is valid it means that rowCount is
        returning the number of children of parent.
        """
        return len(self._list)

    # @overrides
    def data(self, index: QModelIndex, role: Qt.DisplayRole) -> str | None:
        """doc"""
        if role != Qt.DisplayRole:
            return None
        return self._list[index.row()].name()
