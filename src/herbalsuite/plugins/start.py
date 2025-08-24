
from PySide6 import QtWidgets, QtCore
from . import register

@register("home")
def make():
    w = QtWidgets.QWidget()
    g = QtWidgets.QGridLayout(w)
    # Begrüßung
    hello = QtWidgets.QLabel("Guten Morgen, Willkommen in HerbalSuite!")
    hello.setStyleSheet("font-size:20px; font-weight:600;")
    g.addWidget(hello, 0, 0, 1, 2)
    # Heutige Termine (Platzhalter)
    appt = QtWidgets.QGroupBox("Heutige Termine")
    appt.setLayout(QtWidgets.QVBoxLayout())
    appt.layout().addWidget(QtWidgets.QLabel("(Keine Termine eingetragen)"))
    g.addWidget(appt, 1, 0)
    # Aufgabenliste (Platzhalter)
    tasks = QtWidgets.QGroupBox("Aufgaben")
    tasks.setLayout(QtWidgets.QVBoxLayout())
    tasks.layout().addWidget(QtWidgets.QLabel("(Keine Aufgaben)") )
    g.addWidget(tasks, 1, 1)
    # Heilpflanzen-Sektion (Platzhalter)
    herbs = QtWidgets.QGroupBox("Heilpflanzen")
    herbs.setLayout(QtWidgets.QHBoxLayout())
    for name in ["Echinacea", "Kamille", "Pfefferminze", "Süßholz"]:
        herbs.layout().addWidget(QtWidgets.QPushButton(name))
    g.addWidget(herbs, 2, 0, 1, 2)
    g.setRowStretch(3, 1)
    return w
