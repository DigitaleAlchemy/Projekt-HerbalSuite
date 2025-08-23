# -*- coding: utf-8 -*-

"""
HerbalSuite – GUI Bootstrap (PyQt6 + QML)
-----------------------------------------
Dieses Skript startet die Neo‑Botanical QML‑App‑Shell innerhalb
eines QMainWindow (QQuickWidget als Zentral-Widget).

Voraussetzungen:
 - PyQt6 (getestet mit 6.9.1)
 - Ordnerstruktur:
   app/
     lib/
       models/schedule_model.py
       i18n/de-DE.json
     ui/AppShell.qml

Start:
 python "herbalsuite_gui.py"
"""

import sys, json
from pathlib import Path
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu
from PyQt6.QtQuickWidgets import QQuickWidget

# High-DPI (unter Qt6 sind manche Flags no-op; try/except)
def enable_high_dpi() -> None:
    try:
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    except AttributeError:
        pass
    try:
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        pass

# Pfade & i18n
REPO_ROOT = Path(__file__).resolve().parent
APP_DIR = REPO_ROOT / 'app'
LIB_DIR = APP_DIR / 'lib'
UI_DIR = APP_DIR / 'ui'
I18N_DIR = LIB_DIR / 'i18n'

# Damit "from models.schedule_model import ScheduleModel" funktioniert
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

def load_i18n(locale: str = 'de-DE') -> dict:
    path = I18N_DIR / f'{locale}.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# MainWindow mit QML im Zentrum
class HerbalSuiteMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('HerbalSuite')
        self.resize(1280, 800)

        # Menüleiste
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        file_menu = QMenu('Datei', self)
        menu_bar.addMenu(file_menu)

        # QML in QWidget einbetten
        quick = QQuickWidget(self)
        quick.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)

        # Kontext-Objekte bereitstellen
        from models.schedule_model import ScheduleModel
        quick.rootContext().setContextProperty('I18N', load_i18n('de-DE'))
        quick.rootContext().setContextProperty('scheduleModel', ScheduleModel())

        # AppShell laden
        qml_file = UI_DIR / 'AppShell.qml'
        quick.setSource(QUrl.fromLocalFile(str(qml_file)))

        # QML-View als zentralen Bereich setzen
        self.setCentralWidget(quick)

def main() -> None:
    enable_high_dpi()
    app = QApplication(sys.argv)
    app.setApplicationDisplayName('HerbalSuite')
    win = HerbalSuiteMainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
