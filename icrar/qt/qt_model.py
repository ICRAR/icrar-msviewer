
from abc import abstractmethod
from overrides import overrides
from PySide6.QtCore import QObject, Signal


class INotifyPropertyChanged:
    """
    Provides a standard interface for OneWay or TwoWay data
    binding between models and views.
    """
    @property
    @abstractmethod
    def onPropertyChanged(self) -> Signal:
        """
        Provides a subscribable signal triggered
        when instance properties change.
        """


class QtModel(QObject, INotifyPropertyChanged):
    """
    Model containing state per open measurement set
    """
    _onPropertyChanged = Signal(str)

    @property
    @overrides
    def onPropertyChanged(self):
        return self._onPropertyChanged
