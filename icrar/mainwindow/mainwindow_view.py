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
from typing import List, Type, TypeVar

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView,
    QListView,
    QLineEdit, QSplitter, QFileDialog,
    QStatusBar, QProgressBar, QToolTip,
    QTabWidget, QWidget, QAbstractItemView, QMessageBox
)
from PySide6.QtCore import (
    QFile,
    Slot,
    Signal,
    QItemSelection,
    QModelIndex
)

from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction, QIcon
from icrar.listmodel.ms_list_model import MSListModel

from icrar.mainwindow.mainwindow_model import MainWindowModel
from icrar.mainwindow.mainwindow_viewmodel import MainWindowViewModel
from icrar.msinfowidget.msinfowidget_view import MSInfoWidget

T = TypeVar('T')

class MainWindow(QMainWindow):
    """
    Main window view bindings of icrar ms viewer.
    Current primary responsibility is displaying table view.
    Binding to viewmodels is performed via code.
    Views contain the app heirarchy/backbone.
    Views always own a single viewmodel context.

    To modify the ui in Qt Designer change the widget class from MainWindow to QMainWindow
    (the designer does not allow overriding QMainWindow)
    """
    _viewmodel: MainWindowViewModel
    tableview: QTableView
    listview: QListView
    queryedit: QLineEdit

    def __init__(self, parent=None):
        super().__init__(parent)
        self._viewmodel = MainWindowViewModel(self.centralWidget(), MainWindowModel())

    @property
    def viewmodel(self):
        """Returns the viewmodel"""
        return self._viewmodel

    def getChild(self, t: Type[T], name = None) -> T:
        return super().findChild(t, name)  # type: ignore

    def initialize(self):
        """Must be called after ui loading"""
        self.listview = self.getChild(QListView)
        
        # Table Data
        self.tabledatatab = self.getChild(QWidget, "tab_1")
        self.tableview = self.tabledatatab.findChild(QTableView)
        self.queryedit = self.tabledatatab.findChild(QLineEdit)
        # Table Desc
        self.tabledesctab = self.getChild(QWidget, "tab_2")
        self.msinfowidget = self.getChild(MSInfoWidget)
        # DM Info
        self.dminfotab = self.getChild(QWidget, "tab_3")
        # Gridding
        self.griddingtab = self.getChild(QWidget, "tab_4")

        # layout
        self.getChild(QSplitter).setStretchFactor(1,1)
        self.getChild(QTabWidget).setCurrentIndex(0)

        # bindings
        # Since Qt XML does not have binding syntax, if the model gets reassigned
        # then child view components must  refech fetch the model.
        # update view model references and trigger handlers
        self.update_listmodel(self.viewmodel.listmodel)

        # custom viewmodel signals
        self.viewmodel.on_list_model_set.connect(self.update_listmodel)
        self.viewmodel.on_table_model_set.connect(self.update_tablemodel)
        self.viewmodel.on_status_message.connect(self.statusBar().showMessage)
        #self.viewmodel.on_query_failed.connect(self.query_failed)

    @Slot()
    def show_about(self):
        with open(pathlib.Path(__file__).parent.resolve()/"COPYRIGHT", 'r', encoding='utf-8') as f:
            QMessageBox.about(self.centralWidget(), "About", f.read())

    @Slot(MSListModel)
    def update_listmodel(self, model: MSListModel):
        """doc"""
        self.listview.setModel(model)
        # TODO: could moved to viewmodel
        self.listview.selectionModel().selectionChanged.connect(self.select_active_ms)

    @Slot()
    def update_tablemodel(self):
        """doc"""
        self.tableview.setModel(self.viewmodel.tablemodel)

    @Slot()
    def open_ms(self): #open_ms_dialog
        """
        Runs a file dialog and triggers a measurement set load then
        reruns the measurement set query.
        """
        # TODO: ideally these belong in the viewmodel
        ms_path = QFileDialog.getExistingDirectory(self.centralWidget())
        if ms_path:
            self.viewmodel.load_ms(ms_path)
            self.update_query()

    @Slot(QItemSelection, QItemSelection)
    def select_active_ms(self, selected: QItemSelection, deselected: QItemSelection):
        """doc"""
        if len(selected.indexes()) == 1:
            self.viewmodel.select_ms(selected.indexes()[0].row())

    @Slot()
    def update_query(self):
        """Passes the query text to the view model"""
        try:
            self.viewmodel.taqlquery = self.queryedit.text()
            QToolTip.hideText()
        except RuntimeError as e:
            # TODO: move to queryfailed slot so try-except is in viewmodel
            QToolTip.showText(self.queryedit.mapToGlobal(self.queryedit.pos()), str(e))

    @Slot()
    def handle_query_passed(self):
        QToolTip.hideText()

    @Slot(str)
    def handle_query_failed(self, message: str):
        QToolTip.showText(self.queryedit.mapToGlobal(self.queryedit.pos()), message)

    @Slot(QModelIndex)
    def testslot(self, index: QModelIndex):
        print(f"Test Slot! {index}")
