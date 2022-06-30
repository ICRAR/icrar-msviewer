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
import os
from pathlib import Path
import pathlib
from typing import Callable

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView,
    QListView, QVBoxLayout,
    QLineEdit, QSplitter, QFileDialog,
    QStatusBar, QProgressBar, QToolTip,
    QTabWidget, QWidget, QAbstractItemView,
    QMessageBox, QPlainTextEdit, QPlainTextDocumentLayout,
    QSizePolicy
)
from PySide6.QtCore import (
    QFile,
    Slot,
    QItemSelection,
    QRect,
    Qt,
    QObject
)
from PySide6.QtUiTools import QUiLoader, loadUiType
from PySide6.QtGui import QAction, QTextDocument, QPainter, QBrush, QColor

from icrar.mainwindow.mainwindow_model import MainWindowModel

from icrar.msinfowidget.msinfowidget_viewmodel import MSInfoViewModel


class StringAttrModel(QObject):
    """A viewmodel that observes a single string"""
    _model: QObject
    _attrib: str
    _getter: Callable

    def __init__(self, model, attrib):
        self._model = model
        self._attrib = attrib

    def data(self):
        return self._model.getattr(self._attrib)


class MSInfoWidget(QWidget):
    """
    Main window view bindings of icrar ms viewer.
    Current primary responsibility is displaying table view.
    Binding to viewmodels is performed via code.
    Views contain the app heirarchy/backbone.
    Views always own a single viewmodel context.
    """
    _viewmodel: MSInfoViewModel | None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_ui()

    def setModel(self, model: MainWindowModel):
        self._viewmodel = MSInfoViewModel(model, self)
        self._viewmodel.descChanged.connect(self.handle_table_changed)

    @property
    def viewmodel(self):
        """Returns the viewmodel"""
        return self._viewmodel

    # @viewmodel.setter
    # def viewmodel(self, value):
    #     self._viewmodel = value

    def load_ui(self):
        """_summary_
        """
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "msinfowidget.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        self.setLayout(QVBoxLayout())
        child = self.findChild(QWidget)
        self.layout().addWidget(child)

    def handle_table_changed(self):
        if self.viewmodel is not None:
            print(self.viewmodel._model.selected_tables)
            self.findChild(QLineEdit, "channelstext").setText(str(self.viewmodel.channels))
            self.findChild(QLineEdit, "stationstext").setText(str(self.viewmodel.stations))
            self.findChild(QLineEdit, "antennastext").setText(str(self.viewmodel.model_antennas))
            self.findChild(QLineEdit, "baselinestext").setText(str(self.viewmodel.baselines))
            self.findChild(QLineEdit, "timestepstext").setText(str(self.viewmodel.timesteps))
            self.findChild(QLineEdit, "autoctext").setText(str(self.viewmodel.has_autocorrelations))
