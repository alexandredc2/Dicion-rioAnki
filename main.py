import sys
from database.connection import DatabaseManager
from PyQt5.QtWidgets import QApplication
from ui.main_window2 import MainWindow

if __name__ == "__main__":
    banco = DatabaseManager()
    app = QApplication(sys.argv)
    window = MainWindow(banco)
    window.show()
    sys.exit(app.exec_())