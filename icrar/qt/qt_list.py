
from PySide6.QtCore import QObject, Signal

class QtList(QObject):
    """
    An observable list that emits a signal when modified.
    """
    _list: list
    itemsChanged: Signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._list = list()

    def append(self, *args, **kwargs):
        self._list.append(*args, **kwargs)
        self.itemsChanged.emit()

    def insert(self, *args, **kwargs):
        self._list.insert(*args, **kwargs)
        self.itemsChanged.emit()

    def pop(self, *args, **kwargs):
        result = self._list.pop(*args, **kwargs)
        self.itemsChanged.emit()
        return result

    def clear(self, *args, **kwargs):
        self._list.clear(*args, **kwargs)
        self.itemsChanged.emit()

    def __len__(self):
        return self._list.__len__()

    def __getitem__(self, i):
        return self._list[i]

    def __repr__(self):
        return self._list.__repr__()

    def __str__(self):
        return self._list.__str__()
