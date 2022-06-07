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
    Qt
)
from PySide6.QtUiTools import QUiLoader, loadUiType
from PySide6.QtGui import QAction, QTextDocument, QPainter, QBrush, QColor

from icrar.mainwindow.mainwindow_model import MainWindowModel
from icrar.mainwindow.mainwindow_viewmodel import MainWindowViewModel
from icrar.mplcanvaswidget.mpl_canvas_widget import MplCanvasWidget


class TabDescWidget(QWidget):
    """
    Main window view bindings of icrar ms viewer.
    Current primary responsibility is displaying table view.
    Binding to viewmodels is performed via code.
    Views contain the app heirarchy/backbone.
    Views always own a single viewmodel context.
    """
    _viewmodel: MainWindowViewModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_ui()

    @property
    def viewmodel(self):
        """Returns the viewmodel"""
        return self._viewmodel

    def load_ui(self):
        """_summary_
        """
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "tabdescwidget.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        self.setLayout(QVBoxLayout())
        child = self.findChild(QWidget)
        self.layout().addWidget(child)

    # def paintEvent(self, e):
    #     painter = QPainter(self)

    #     brush = QBrush()
    #     brush.setColor(QColor('black'))
    #     brush.setStyle(Qt.SolidPattern)
    #     rect = QRect(0, 0, painter.device().width(), painter.device().height())
    #     painter.fillRect(rect, brush)
