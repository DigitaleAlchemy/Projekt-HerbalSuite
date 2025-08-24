
from PySide6 import QtWidgets
from . import register

@register("patients")
def make():
    w = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(w)
    layout.addWidget(QtWidgets.QLabel("Patientenverwaltung (MVP)") )
    toolbar = QtWidgets.QHBoxLayout()
    toolbar.addWidget(QtWidgets.QPushButton("Neu"))
    toolbar.addWidget(QtWidgets.QPushButton("Bearbeiten"))
    toolbar.addWidget(QtWidgets.QPushButton("Suchen"))
    toolbar.addStretch(1)
    layout.addLayout(toolbar)
    table = QtWidgets.QTableWidget(0, 4)
    table.setHorizontalHeaderLabels(["Nachname", "Vorname", "Geburtsdatum", "Patienten-ID"]) 
    layout.addWidget(table)
    return w
