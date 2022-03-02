from overrides import overrides
from pandas import DataFrame

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QPersistentModelIndex, SIGNAL


class PandasTableModel(QAbstractTableModel):
    """
    https://stackoverflow.com/questions/19411101/pyside-qtableview-example
    """
    def __init__(self, parent, df: DataFrame, *args):
        """doc"""
        super().__init__(parent)
        self.df = df # DataFrame& const df; pointer is not allowed to be reassigned
        self.header = self.df.columns

        # Experimental
        self._showindex = True

    # @overrides
    def rowCount(self, parent) -> int:
        """doc"""
        return self.df.shape[0]

    # @overrides
    def columnCount(self, parent) -> int:
        """doc"""
        return self.df.shape[1] if not self._showindex else self.df.shape[1] + 1

    # @overrides
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> str | None:
        """doc"""
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        if not self._showindex:
            return str(self.df.iloc[index.row(),index.column()])
        else:
            return str(self.df.index[index.row()]) if index.column() == 0 else str(self.df.iloc[index.row(),index.column()-1])

    # @overrides
    def headerData(self, col, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """doc"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if not self._showindex:
                return self.header[col]
            else:
                return 'index' if col == 0 else self.header[col-1]
        return None

    # @overrides
    def sort(self, col: int, order: Qt.SortOrder):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        if not self._showindex:
            self.df.sort_values(by=self.df.columns[col], inplace=True, ascending=(order == Qt.AscendingOrder))
        else:
            if col > 0:
                self.df.sort_values(by=self.df.columns[col-1], inplace=True, ascending=(order == Qt.AscendingOrder))
            else:
                self.df.sort_index(inplace=True, ascending=(order == Qt.AscendingOrder))
        self.emit(SIGNAL("layoutChanged()"))

    # @overrides
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """docs"""
        default = Qt.ItemNeverHasChildren | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        if not self._showindex:
            return default
        else:
            return default if index.column() > 0 else Qt.ItemNeverHasChildren

    def setData(self, index, value, role: Qt.EditRole):
        """docs"""
        index_column = index.column() if not self._showindex else index.column() - 1
        datatype = self.df[self.df.columns[index_column]].dtype
        try:
            self.df.iloc[index.row(), index_column] = datatype.type(value)
            return True
        except ValueError:
            return False