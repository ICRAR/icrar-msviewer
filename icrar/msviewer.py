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
import pathlib
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QCoreApplication, QFile
from PySide6.QtGui import QIcon
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtUiTools import QUiLoader
from icrar.mainwindow.mpl_canvas_widget import MplCanvasWidget

from icrar.mainwindow.mainwindow_view import MainWindow

def main():
    QQuickWindow.setGraphicsApi(QSGRendererInterface.OpenGLRhi)
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(pathlib.Path(__file__).parent.resolve()/"icon.ico")))

    loader = QUiLoader()
    loader.registerCustomWidget(MainWindow)
    loader.registerCustomWidget(MplCanvasWidget)
    path = os.fspath(pathlib.Path(__file__).resolve().parent / "mainwindow/mainwindow.ui")
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    loader.load(ui_file, None)
    window: MainWindow = loader.load(path, None)  # type: ignore
    window.initialize()

    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            window.viewmodel.load_ms(sys.argv[i])
    window.queryedit.setText("SELECT * FROM $1 LIMIT 1000000")
    window.update_query()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
