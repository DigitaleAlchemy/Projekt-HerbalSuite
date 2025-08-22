from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QMenuBar, QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
import sys

class HerbalSuiteMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HerbalSuite")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #f0f4f7;")

        # Create menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Add menus
        file_menu = QMenu("Datei", self)
        module_menu = QMenu("Module", self)
        help_menu = QMenu("Hilfe", self)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(module_menu)
        menu_bar.addMenu(help_menu)

        # Add actions to menus
        exit_action = QAction("Beenden", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # HerbalSuite Logo placeholder
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setText("🌿 HerbalSuite")
        logo_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2e7d32; margin-top: 40px;")

        # Welcome text
        welcome_label = QLabel("Willkommen bei HerbalSuite – Ihre modulare Heilpflanzen-Software")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; color: #555; margin-bottom: 20px;")

        layout.addWidget(logo_label)
        layout.addWidget(welcome_label)

        central_widget.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = HerbalSuiteMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
