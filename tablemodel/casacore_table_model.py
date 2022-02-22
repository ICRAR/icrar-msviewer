from typing import List
from overrides import overrides
from casacore.tables import table as Table

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, SIGNAL

class CasacoreTableModel(QAbstractTableModel):
    """
    https://stackoverflow.com/questions/19411101/pyside-qtableview-example
    """
    _table: Table
    _querytable: Table | None = None

    def __init__(self, parent, table: Table, *args):
        """doc"""
        super().__init__(parent)
        self._table = table
        self._querytable = self._table

        # Experimental
        self._showindex = True

    @property
    def table(self):
        """doc"""
        return self._table

    @property
    def querytable(self):
        """doc"""
        return self._querytable
    
    @querytable.setter
    def querytable(self, value):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self._querytable = value
        self.emit(SIGNAL("layoutChanged()"))

    # @overrides
    def rowCount(self, parent) -> int:
        """doc"""
        return self._querytable.nrows() if self._querytable else 0

    # @overrides
    def columnCount(self, parent) -> int:
        """doc"""
        if not self._querytable:
            return 0
        return self._querytable.ncols() + 1 if self._showindex else self._querytable.ncols()

    # @overrides
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> str | None:
        """doc"""
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        if not self._querytable:
            return None
        if not self._showindex:
            return str(self._querytable[index.row()][self._querytable.colnames()[index.column()]])
        else:
            return self._querytable.rownumbers()[index.row()] if index.column() == 0 else str(self._querytable[index.row()][self._querytable.colnames()[index.column()-1]])

    # @overrides
    def headerData(self, col, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """doc"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if not self._showindex:
                return self._querytable.colnames()[col]
            else:
                return 'index' if col == 0 else self._querytable.colnames()[col-1]
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
        default = Qt.ItemNeverHasChildren | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        if not self._showindex:
            return default
        else:
            return default if index.column() > 0 else Qt.ItemNeverHasChildren

    # @overrides
    def setData(self, index, value, role: Qt.ItemDataRole):
        """docs"""
        datatype = self.df[self.df.columns[index.column()]].dtype
        try:
            self.df.iloc[index.row(), index.column()] = datatype.type(value)
            return True
        except ValueError:
            return False