# -*- coding: utf-8 -*-
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtGui import QBrush, QColor
from herbalsuite.data.models import Patient

class PatientTableModel(QAbstractTableModel):
    COLUMNS = ["Nachname", "Vorname", "Geburtsdatum", "Telefon", "E‑Mail", "Ort", "Rechnung"]

    def __init__(self, patients: list[Patient]):
        super().__init__()
        self._patients = patients

    def setPatients(self, patients: list[Patient]):
        self.beginResetModel()
        self._patients = patients
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._patients)

    def columnCount(self, parent=QModelIndex()):
        return len(self.COLUMNS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        p = self._patients[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0: return p.last_name or ""
            if col == 1: return p.first_name or ""
            if col == 2: return p.date_of_birth.strftime("%d.%m.%Y") if p.date_of_birth else ""
            if col == 3: return p.phone or p.mobile or ""
            if col == 4: return p.email or ""
            if col == 5: return p.city or ""
            if col == 6: return "Offen" if p.has_open_invoice else "—"

        if role == Qt.ForegroundRole and col == 6 and p.has_open_invoice:
            return QBrush(QColor("#C62828"))

        if role == Qt.TextAlignmentRole and col == 6:
            return Qt.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.COLUMNS[section]
        return None

    def patient_at(self, row: int) -> Patient:
        return self._patients[row]
