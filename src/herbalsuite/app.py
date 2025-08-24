from PySide6 import QtWidgets
from .ui.main_window import MainWindow
from .data.db import Base, engine
from .data.migrate import migrate_patients

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("HerbalSuite")
    # Basic Fusion theme for a clean look
    QtWidgets.QApplication.setStyle("Fusion")

    # --- DB-Setup & Migration ---
    Base.metadata.create_all(bind=engine)
    migrate_patients()
    # ----------------------------

    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
