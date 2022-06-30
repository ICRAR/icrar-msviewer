
from PySide6.QtCore import QObject, Signal, Slot, QModelIndex
from casacore.tables import taql, table as Table

from icrar.mainwindow.mainwindow_model import MainWindowModel

class MSInfoViewModel(QObject):
    _model: MainWindowModel

    #descChanged = Signal()

    def __init__(self, model: MainWindowModel, parent: QObject):
        super().__init__(parent)
        self._model = model
        #self._model.selected_tables.itemsChanged.connect(self.descChanged.emit)

    @property
    def table(self) -> Table | None:
        return self._model.selected_table

    @property
    def rows(self) -> int:
        if self.table:
            return self.table.nrows()
        else:
            return 0

    @property
    def stations(self) -> int:
        """number of stations registered for antenna indexes"""
        if self.table:
            return Table(self.table.getkeyword("ANTENNA"), readonly=True, ack=False).nrows()
        else:
            return 0

    @property
    def model_antennas(self) -> int:
        """number of stations used by antenna columns"""
        if self.table:
            return len(set.union(set(self.table.getcol("ANTENNA1")), set(self.table.getcol("ANTENNA2"))))
        else:
            return 0

    @property
    def polarizations(self) -> int:
        if self.table:
            return self.table.query(columns="DATA",limit=1).getcol("DATA").shape[0]
        else:
            return 0

    @property
    def channels(self) -> int:
        if self.table:
            return self.table.query(columns="DATA",limit=1).getcol("DATA").shape[1]
        else:
            return 0

    @property
    def baselines(self) -> int:
        if self.table:
            num_stations = self.model_antennas
            autocorrelations = self.has_autocorrelations
            return int(num_stations * ((num_stations + 1) / 2 if autocorrelations else (num_stations - 1) / 2))
        else:
            return 0

    @property
    def timesteps(self) -> float:
        if self.table:
            return self.rows / self.baselines
        else:
            return 0

    @property
    def has_autocorrelations(self) -> bool:
        if self.table:
            return (self.table.getcol("ANTENNA1") == self.table.getcol("ANTENNA2")).any()
        else:
            return False

    @property
    def tab_desc(self) -> str:
        return ""

class MsInfoViewModel(QObject):
    pass