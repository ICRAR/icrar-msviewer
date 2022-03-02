
from PySide6.QtCore import QObject, Signal, Slot
from casacore.tables import table as Table

class MSInfoViewModel(QObject):
    _table : Table | None

    def __init__(self):
        pass

    @property
    def table(self) -> Table | None:
        return self._table

    @table.setter
    def table(self, value: Table | None):
        _table = value

    @property
    def rows(self) -> int:
        return self._table.nrows() if self._table else 0

    @property
    def stations(self) -> int:
        return 0

    @property
    def model_antennas(self) -> int:
        """number of stations used by antenna columns"""
        return 0

    @property
    def channels(self) -> int:
        return 0

    @property
    def baselines(self) -> int:
        return 0

    @property
    def has_autocorrelations(self) -> int:
        return 0