
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QComboBox, QTextEdit,
    QDateEdit, QVBoxLayout, QMessageBox, QCheckBox
)
from PySide6.QtCore import QDate
from datetime import date
from herbalsuite.data.models import Patient

SEX_CHOICES = [
    ("",  "—"),
    ("m", "männlich"),
    ("w", "weiblich"),
    ("d", "divers"),
    ("x", "ohne Angabe"),
    ("u", "unbekannt"),
]

class PatientDialog(QDialog):
    def __init__(self, session, patient: Patient | None = None, parent=None):
        super().__init__(parent)
        self.session = session
        self.patient = patient
        self.setWindowTitle("Patient anlegen" if patient is None else "Patient bearbeiten")

        self.first_name = QLineEdit(); self.last_name  = QLineEdit()

        self.dob = QDateEdit(calendarPopup=True)
        self.dob.setDisplayFormat("dd.MM.yyyy"); self.dob.setSpecialValueText("—")
        self.dob.setDateRange(QDate(1900,1,1), QDate.currentDate())

        self.sex = QComboBox(); self.sex.setEditable(False)
        for val, label in SEX_CHOICES:
            self.sex.addItem(label, userData=val)

        self.phone  = QLineEdit(); self.mobile = QLineEdit(); self.email  = QLineEdit()
        self.street = QLineEdit(); self.postal_code = QLineEdit(); self.city = QLineEdit()

        self.chief_complaint = QTextEdit(); self.allergies = QTextEdit(); self.medications = QTextEdit()
        self.diagnoses = QTextEdit(); self.family_history = QTextEdit(); self.lifestyle = QTextEdit(); self.notes = QTextEdit()

        self.has_open_invoice = QCheckBox("Offene Rechnung vorhanden")

        form = QFormLayout()
        form.addRow("Vorname*", self.first_name); form.addRow("Nachname*", self.last_name)
        form.addRow("Geburtsdatum", self.dob); form.addRow("Geschlecht", self.sex)
        form.addRow("Telefon", self.phone); form.addRow("Mobil", self.mobile); form.addRow("E‑Mail", self.email)
        form.addRow("Straße & Nr.", self.street); form.addRow("PLZ", self.postal_code); form.addRow("Ort", self.city)
        form.addRow("Hauptbeschwerde", self.chief_complaint); form.addRow("Allergien", self.allergies)
        form.addRow("Medikamente", self.medications); form.addRow("Diagnosen", self.diagnoses)
        form.addRow("Familienanamnese", self.family_history); form.addRow("Lebensstil", self.lifestyle); form.addRow("Notizen", self.notes)
        form.addRow(self.has_open_invoice)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.on_save); buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self); layout.addLayout(form); layout.addWidget(buttons)
        self._load_patient()

    def _load_patient(self):
        p = self.patient
        if not p:
            self.dob.setDate(QDate(2000,1,1)); self.has_open_invoice.setChecked(False); return
        self.first_name.setText(p.first_name or ""); self.last_name.setText(p.last_name or "")
        if p.date_of_birth:
            self.dob.setDate(QDate(p.date_of_birth.year, p.date_of_birth.month, p.date_of_birth.day))
        idx = self.sex.findData(p.sex or ""); self.sex.setCurrentIndex(max(0, idx))
        self.phone.setText(p.phone or ""); self.mobile.setText(p.mobile or ""); self.email.setText(p.email or "")
        self.street.setText(p.street or ""); self.postal_code.setText(p.postal_code or ""); self.city.setText(p.city or "")
        self.chief_complaint.setPlainText(p.chief_complaint or ""); self.allergies.setPlainText(p.allergies or ""); self.medications.setPlainText(p.medications or "")
        self.diagnoses.setPlainText(p.diagnoses or ""); self.family_history.setPlainText(p.family_history or ""); self.lifestyle.setPlainText(p.lifestyle or ""); self.notes.setPlainText(p.notes or "")
        self.has_open_invoice.setChecked(bool(p.has_open_invoice))

    def _validate(self) -> bool:
        if not self.first_name.text().strip() or not self.last_name.text().strip():
            QMessageBox.warning(self, "Validierung", "Vor- und Nachname sind Pflichtfelder.")
            return False
        email = self.email.text().strip()
        if email and ("@" not in email or "." not in email.split("@")[-1]):
            QMessageBox.warning(self, "Validierung", "Bitte eine gültige E‑Mail-Adresse eingeben.")
            return False
        return True

    def on_save(self):
        if not self._validate(): return
        qd = self.dob.date(); dob = date(qd.year(), qd.month(), qd.day()) if self.dob.date().isValid() else None
        sex_value = self.sex.currentData() or None
        p = self.patient or Patient()
        p.first_name = self.first_name.text().strip(); p.last_name = self.last_name.text().strip()
        p.date_of_birth = dob; p.sex = sex_value
        p.phone = self.phone.text().strip() or None; p.mobile = self.mobile.text().strip() or None; p.email = self.email.text().strip() or None
        p.street = self.street.text().strip() or None; p.postal_code = self.postal_code.text().strip() or None; p.city = self.city.text().strip() or None
        p.chief_complaint = self.chief_complaint.toPlainText().strip() or None
        p.allergies = self.allergies.toPlainText().strip() or None
        p.medications = self.medications.toPlainText().strip() or None
        p.diagnoses = self.diagnoses.toPlainText().strip() or None
        p.family_history = self.family_history.toPlainText().strip() or None
        p.lifestyle = self.lifestyle.toPlainText().strip() or None
        p.notes = self.notes.toPlainText().strip() or None
        p.has_open_invoice = self.has_open_invoice.isChecked()
        self.session.add(p); self.session.commit(); self.patient = p; self.accept()
