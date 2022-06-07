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
from typing import Type, TypeVar

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
    QItemSelection
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction, QIcon

from icrar.mainwindow.mainwindow_model import MainWindowModel
from icrar.mainwindow.mainwindow_viewmodel import MainWindowViewModel

T = TypeVar('T')

class MainWindow(QMainWindow):
    """
    Main window view bindings of icrar ms viewer.
    Current primary responsibility is displaying table view.
    Binding to viewmodels is performed via code.
    Views contain the app heirarchy/backbone.
    Views always own a single viewmodel context.
    """
    _viewmodel: MainWindowViewModel

    def __init__(self, parent=None):
        super().__init__(parent)
        self._viewmodel = MainWindowViewModel(self.centralWidget(), MainWindowModel())
        #self.load_ui()


    @property
    def viewmodel(self):
        """Returns the viewmodel"""
        return self._viewmodel

    def findChild(self, t: Type, name = None) -> Type:
        return super().findChild(t, name)  # type: ignore

    def load_ui(self):
        """_summary_
        """
        # status bar
        self.viewmodel.on_status_message.connect(self.statusBar().showMessage)
        
        #self.statusProgressBar = QProgressBar(self.centralWidget())
        #self.statusProgressBar.setValue(0)
        #self.statusBar().addPermanentWidget(self.statusProgressBar)

        # layout
        self.findChild(QSplitter).setStretchFactor(1,1)

        # bindings
        # Since Qt XML has binding not have binding syntax, if the model gets reassigned
        # then child view components should fetch the model.
        self.tableview = self.findChild(QTableView)
        self.listview = self.findChild(QListView)
        self.queryedit = self.findChild(QLineEdit)
        self.openaction = self.findChild(QAction, "actionOpen_MS")
        self.aboutaction = self.findChild(QAction, "actionAbout")
        

        # update view model references and trigger handlers
        self.update_listmodel()
        self.update_tablemodel()

        # handlers
        self.viewmodel.on_list_model_set.connect(self.update_listmodel)
        self.viewmodel.on_table_model_set.connect(self.update_tablemodel)
        self.listview.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listview.selectionModel().selectionChanged.connect(self.table_selection_changed)

        # commands
        self.openaction.triggered.connect(self.open_ms)
        self.aboutaction.triggered.connect(self.show_about)

        # two-way binding
        self.queryedit.editingFinished.connect(self.run_query)
        #self.viewmodel.query_changed.connect(self.queryedit.setText)

        # qsplitter
        self.tabwidget = self.findChild(QTabWidget)
        self.tabwidget.setCurrentIndex(0)

    @Slot()
    def show_about(self):
        with open(pathlib.Path(__file__).parent.resolve()/"COPYRIGHT", 'r') as f:
            QMessageBox.about(self.centralWidget(), "About", f.read())

    @Slot()
    def update_listmodel(self):
        """doc"""
        self.listview.setModel(self.viewmodel.listmodel)

    @Slot()
    def update_tablemodel(self):
        """doc"""
        self.tableview.setModel(self.viewmodel.tablemodel)

    def table_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        """doc"""
        if len(selected.indexes()) == 1:
            self.viewmodel.select_ms(selected.indexes()[0].row())

    @Slot()
    def open_ms(self):
        """
        Runs a file dialog and triggers a measurement set load then
        reruns the measurement set query.
        """
        ms_path = QFileDialog.getExistingDirectory(self.centralWidget())
        if ms_path:
            self.viewmodel.load_ms(ms_path)
            self.run_query()

    @Slot()
    def run_query(self):
        """Passes the query text to the view model"""
        try:
            self.viewmodel.taqlquery = self.queryedit.text()
            QToolTip.hideText()
        except RuntimeError as e:
            # TODO: move to viewmodel.queryfailed handler
            QToolTip.showText(self.queryedit.mapToGlobal(self.queryedit.pos()), str(e))
