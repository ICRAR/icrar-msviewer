# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
from typing import Any
import sys
from overrides import overrides

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView,
    QLineEdit, QSplitter, QFileDialog,
    QStatusBar, QProgressBar, QToolTip,
    QTabWidget, QWidget
)
from PySide6.QtCore import (
    QObject, QFile, QAbstractTableModel,
    Qt, QCoreApplication, Signal,
    QModelIndex, QPersistentModelIndex, SIGNAL,
    Slot
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction, QIcon

from casacore.tables import table as Table
from mainwindow.mainwindow_viewmodel import MainWindowViewModel
from mpl_canvas_widget import MplCanvasWidget

from tablemodel.casacore_table_model import CasacoreTableModel
from tablemodel.pandas_table_model import PandasTableModel


class MainWindow(QMainWindow):
    """
    Main window component of icrar casacore explorer.
    Current primary responsibility is displaying table view.
    Binding to viewmodels is performed via code.
    Views contain the app heirarchy/backbone.
    Views always own a single viewmodel context.
    """
    _viewmodel: MainWindowViewModel

    def __init__(self):
        super().__init__()
        self._viewmodel = MainWindowViewModel(self)
        self.load_ui()

        # TODO experimental
        self.tabwidget = self.findChild(QTabWidget)
        self.tabwidget.findChild(QWidget, "tab_3")\
            .layout()\
            .addWidget(MplCanvasWidget(self.tabwidget))
        self.tabwidget.setCurrentIndex(0)

    @property
    def viewmodel(self):
        """Returns the viewmodel"""
        return self._viewmodel

    def load_ui(self):
        """_summary_
        """
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "mainwindow.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        # layout
        self.findChild(QSplitter).setStretchFactor(1,1)

        # print(self.statusBar())
        # print(self.findChild(QStatusBar))
        # print(self.statusBar().isSizeGripEnabled())
        # self.statusBar().setSizeGripEnabled(False)
        # print(self.statusBar().isSizeGripEnabled())
        # self.setStatusBar(self.statusBar())
        #self.statusBar().reformat()
        
        # status = QStatusBar(self)
        # status.resize(self.size().width(), 10)
        # status.showMessage("Welcome!", 10)
        # self.setStatusBar(status)
        #self.statusProgressBar = QProgressBar(self.centralWidget())
        #self.statusBar().addPermanentWidget(self.statusProgressBar)
        #self.statusProgressBar.setValue(51)

        # bindings
        # Since Qt XML has binding not have binding syntax, if the model gets reassigned
        # then child view components should fetch the model.
        self.tableview = self.findChild(QTableView)
        self.queryedit = self.findChild(QLineEdit)
        self.openaction = self.findChild(QAction)

        # handlers
        self.viewmodel.on_model_set.connect(lambda: self.tableview.setModel(self.viewmodel.tablemodel))

        # commands
        self.openaction.triggered.connect(self.open_ms)
        
        # two-way binding
        self.queryedit.editingFinished.connect(self.run_query)
        #self.viewmodel.query_changed.connect(self.queryedit.setText)

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

        self.statusBar().showMessage("Ready", 2000)
        print(self.statusBar().currentMessage())
        self.statusBar().reformat()

    @Slot()
    def run_query(self):
        """Passes the query text to the view model"""
        try:
            self.viewmodel.taqlquery = self.queryedit.text()
            QToolTip.hideText()
        except RuntimeError as e:
            # TODO: move to viewmodel.queryfailed handler
            QToolTip.showText(self.queryedit.mapToGlobal(self.queryedit.pos()), str(e))
