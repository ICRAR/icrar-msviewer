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
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QIcon

from icrar.mainwindow.mainwindow_view import MainWindow

def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.ico"))

    window = MainWindow()
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            window.viewmodel.load_ms(sys.argv[i])
    window.queryedit.setText("SELECT * FROM $1 LIMIT 100000000")
    window.queryedit.editingFinished.emit()
    window.centralWidget().show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
