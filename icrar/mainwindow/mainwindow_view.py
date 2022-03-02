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
from icrar.mainwindow.mpl_canvas_widget import MplCanvasWidget


class MainWindow(QMainWindow):
    """
    Main window view bindings of icrar ms viewer.
    Current primary responsibility is displaying table view.
    Binding to viewmodels is performed via code.
    Views contain the app heirarchy/backbone.
    Views always own a single viewmodel context.
    """
    _viewmodel: MainWindowViewModel

    def __init__(self):
        super().__init__()
        self._viewmodel = MainWindowViewModel(self.centralWidget(), MainWindowModel())
        self.load_ui()

        self.tabwidget = self.findChild(QTabWidget)
        self.tabwidget.setCurrentIndex(0)

    @property
    def viewmodel(self):
        """Returns the viewmodel"""
        return self._viewmodel

    def load_ui(self):
        """_summary_
        """
        loader = QUiLoader()
        loader.registerCustomWidget(MplCanvasWidget)
        path = os.fspath(Path(__file__).resolve().parent / "mainwindow.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        # status bar
        self.statusBar = self.centralWidget().statusBar()
        self.viewmodel.on_status_message.connect(self.statusBar.showMessage)
        
        #self.statusProgressBar = QProgressBar(self.centralWidget())
        #self.statusProgressBar.setValue(0)
        #self.statusBar.addPermanentWidget(self.statusProgressBar)

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

    @Slot()
    def show_about(self):
        with open("COPYRIGHT", 'r') as f:
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
