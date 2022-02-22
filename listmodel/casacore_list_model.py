
from typing import List
from casacore.tables import table as Table
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, SIGNAL

class CasacoreItemModel(QAbstractListModel):
    """Provides a viewmodel for a list of open casacore ms"""
    _list: List[Table]

    def __init__(self, parent, list: List[Table], *args):
        super().__init__(parent)
        self._list = list

    def append(self, item):
        """doc"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self._list.append(item)
        self.emit(SIGNAL("layoutChanged()"))

    # @overrides
    def rowCount(self, parent) -> int:
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