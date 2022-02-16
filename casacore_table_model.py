from ast import List
from overrides import overrides
from casacore.tables import table as Table

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QPersistentModelIndex, SIGNAL

class CasacoreTableModel(QAbstractTableModel):
    """
    https://stackoverflow.com/questions/19411101/pyside-qtableview-example
    """
    def __init__(self, parent, table: Table, *args):
        """doc"""
        super().__init__(parent)
        self.table = table # Table& const table; pointer is not allowed to be reassigned
        # Experimental
        self._showindex = True

    # @overrides
    def rowCount(self, parent) -> int:
        """doc"""
        return self.table.nrows()

    # @overrides
    def columnCount(self, parent) -> int:
        """doc"""
        return self.table.ncols() + 1 if self._showindex else 0

    # @overrides
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> str | None:
        """doc"""
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        if not self._showindex:
            return str(self.table[index.row()][self.table.colnames()[index.column()]])
        else:
            return index.row() if index.column() == 0 else str(self.table[index.row()][self.table.colnames()[index.column()-1]])

    # @overrides
    def headerData(self, col, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """doc"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if not self._showindex:
                return self.table.colnames()[col]
            else:
                return 'index' if col == 0 else self.table.colnames()[col-1]
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