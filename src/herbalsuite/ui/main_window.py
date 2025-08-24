from PySide6 import QtWidgets, QtGui, QtCore
from ..plugins import create_page

SECTIONS = [
    ("Startseite", "home"),
    ("Patienten", "patients"),
    ("Rezepturen", "recipes"),
    ("Diagnostik", "diagnostics"),
    ("Lagerverwaltung", "inventory"),
    ("Einstellungen", "settings"),
]

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HerbalSuite")
        self.resize(1200, 800)
        self._init_ui()

    def _init_ui(self):
        # Sidebar
        self.sidebar = QtWidgets.QListWidget()
        self.sidebar.setFixedWidth(220)
        for label, key in SECTIONS:
            item = QtWidgets.QListWidgetItem(label)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, key)
            self.sidebar.addItem(item)

        # Stacked central widgets
        self.stack = QtWidgets.QStackedWidget()
        self._pages = {}
        for label, key in SECTIONS:
            widget = create_page(key) or self._placeholder(label)
            self._pages[key] = widget
            self.stack.addWidget(widget)

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        # Layout
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(container)

    def _placeholder(self, title: str):
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        text = f"{title}\n\n(Platzhalter – Plugin kann diese Seite ersetzen)"
        lbl = QtWidgets.QLabel(text)
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 18px; color: #556;")
        v.addStretch(1)
        v.addWidget(lbl)
        v.addStretch(2)
        return w
