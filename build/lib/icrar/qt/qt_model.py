
from abc import abstractmethod
from PySide6.QtCore import QObject, Signal


class INotifyPropertyChanged:
    """
    Provides a standard interface for OneWay or TwoWay data
    binding between models and views.
    """
    @property
    @abstractmethod
    def onPropertyChanged(self) -> Signal:
        pass


class QtModel(QObject, INotifyPropertyChanged):
    """
    Model containing state per open measurement set
    """
    _onPropertyChanged = Signal(str)
    @property
    def onPropertyChanged(self):
        return self._onPropertyChanged
