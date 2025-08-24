
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
from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from . import register
from herbalsuite.data.models import Patient, Base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Setup SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class PatientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neuen Patienten anlegen")
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.last_name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.birth_date_input = QLineEdit()
        self.birth_date_input.setPlaceholderText("TT.MM.JJJJ")

        form_layout.addRow("Nachname:", self.last_name_input)
        form_layout.addRow("Vorname:", self.first_name_input)
        form_layout.addRow("Geburtsdatum:", self.birth_date_input)

        layout.addLayout(form_layout)

        save_button = QPushButton("Speichern")
        save_button.clicked.connect(self.save_patient)
        layout.addWidget(save_button)

    def save_patient(self):
        last_name = self.last_name_input.text().strip()
        first_name = self.first_name_input.text().strip()
        birth_date_str = self.birth_date_input.text().strip()

        try:
            birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y").date()
        except ValueError:
            QMessageBox.warning(self, "Fehler", "Geburtsdatum muss im Format TT.MM.JJJJ sein.")
            return

        if not last_name or not first_name:
            QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen.")
            return

        session = SessionLocal()
        new_patient = Patient(last_name=last_name, first_name=first_name, birth_date=birth_date)
        session.add(new_patient)
        session.commit()
        session.close()

        QMessageBox.information(self, "Erfolg", "Patient erfolgreich gespeichert.")
        self.accept()

@register("patients")
def make():
    w = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(w)
    layout.addWidget(QtWidgets.QLabel("Patientenverwaltung (MVP)"))
    toolbar = QtWidgets.QHBoxLayout()

    new_button = QtWidgets.QPushButton("Neu")
    toolbar.addWidget(new_button)
    toolbar.addWidget(QtWidgets.QPushButton("Bearbeiten"))
    toolbar.addWidget(QtWidgets.QPushButton("Suchen"))
    toolbar.addStretch(1)
    layout.addLayout(toolbar)

    table = QtWidgets.QTableWidget(0, 4)
    table.setHorizontalHeaderLabels(["Nachname", "Vorname", "Geburtsdatum", "Patienten-ID"])
    layout.addWidget(table)

    def refresh_table():
        session = SessionLocal()
        patients = session.query(Patient).all()
        table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(patient.last_name))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(patient.first_name))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(patient.birth_date.strftime("%d.%m.%Y")))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(patient.id)))
        session.close()

    def open_patient_dialog():
        dialog = PatientDialog()
        if dialog.exec():
            refresh_table()

    new_button.clicked.connect(open_patient_dialog)
    refresh_table()

    return w
