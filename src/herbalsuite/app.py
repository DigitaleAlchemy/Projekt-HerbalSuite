
from PySide6 import QtWidgets, QtGui
from .ui.main_window import MainWindow

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("HerbalSuite")
    # Basic Fusion theme for a clean look
    QtWidgets.QApplication.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
