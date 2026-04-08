import sys
import os
from database.connection import DatabaseManager
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dicionario.anki")

if __name__ == "__main__":
    banco = DatabaseManager()
    app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "main_ico.ico")
    app.setWindowIcon(QIcon(icon_path))
    window = MainWindow(banco)
    window.show()
    sys.exit(app.exec_())