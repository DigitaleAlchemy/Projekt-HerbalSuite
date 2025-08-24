# -*- coding: utf-8 -*-
"""
Patienten-Dialog mit Kompakt-/Erweitert-Modus.

Kompakt:
- Stammdaten: Nachname*, Vorname*, Straße, PLZ*, Ort*
- Buttons: Erweitern, Termin vergeben, Speichern, Abbrechen

Erweitert:
- Links: zusätzlich Allergien, Anmerkungen
- Rechts: Tabs (Platzhalter) für Hauptbeschwerden, Medikamente, Diagnosen,
          Anamnese, Familienanamnese, Lebensstil, Rechnungen (mit Filter)

Signale:
- patient_saved(Patient): wird nach erfolgreichem Speichern emittiert.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QSplitter, QWidget,
    QLineEdit, QPlainTextEdit, QPushButton, QLabel, QTabWidget, QComboBox,
    QTableView, QMessageBox, QFrame
)
from herbalsuite.data.models import Patient


class PatientDialog(QDialog):
    patient_saved = Signal(object)  # emits Patient instance

    def __init__(self, session, patient: Patient | None = None, parent=None):
        super().__init__(parent)
        self.session = session
        self.patient = patient
        self.is_expanded = False

        self.setWindowTitle("Patient anlegen" if patient is None else "Patient bearbeiten")

        # --- Hauptlayout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        self.title_label = QLabel("Neuen Patienten anlegen" if self.patient is None else "Patientendaten bearbeiten")
        self.title_label.setObjectName("DialogTitle")
        self.subtitle_label = QLabel("Stammdaten (Name bis Ort)")
        self.subtitle_label.setObjectName("DialogSubtitle")
        header_texts = QVBoxLayout()
        header_texts.addWidget(self.title_label)
        header_texts.addWidget(self.subtitle_label)
        header.addLayout(header_texts)
        header.addStretch()
        self.main_layout.addLayout(header)

        # --- Splitter (links Formular, rechts Tabs)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.main_layout.addWidget(self.splitter, 1)

        # ------- Linke Seite
        self.left = QWidget()
        self.left_layout = QVBoxLayout(self.left)
        self.left_layout.setSpacing(10)

        # Kompakt-Formular (Stammdaten)
        self.form_basic = QFormLayout()
        self.form_basic.setLabelAlignment(Qt.AlignRight)
        self.form_basic.setFormAlignment(Qt.AlignTop)

        self.input_lastname = QLineEdit()
        self.input_firstname = QLineEdit()
        self.input_street = QLineEdit()
        self.input_postal_code = QLineEdit()
        self.input_city = QLineEdit()

        # Pflichtfelder visuell markierbar (QSS kann auf [invalid] reagieren)
        for w in (self.input_lastname, self.input_firstname, self.input_postal_code, self.input_city):
            w.setProperty("invalid", False)

        self.form_basic.addRow("Nachname*", self.input_lastname)
        self.form_basic.addRow("Vorname*", self.input_firstname)
        self.form_basic.addRow("Straße & Nr.", self.input_street)
        self.form_basic.addRow("PLZ*", self.input_postal_code)
        self.form_basic.addRow("Ort*", self.input_city)

        self.left_layout.addLayout(self.form_basic)

        # Erweiterte Felder (zunächst ausgeblendet)
        self.expanded_frame = QFrame()
        self.expanded_frame.setObjectName("ExpandedFrame")
        self.expanded_frame.setVisible(False)
        expanded_layout = QFormLayout(self.expanded_frame)
        expanded_layout.setLabelAlignment(Qt.AlignRight)

        self.input_allergies = QPlainTextEdit()
        self.input_notes = QPlainTextEdit()
        self.input_allergies.setPlaceholderText("z. B. Penicillin, Nüsse …")
        self.input_notes.setPlaceholderText("Anmerkungen zur Person, Besonderheiten …")

        expanded_layout.addRow("Allergien", self.input_allergies)
        expanded_layout.addRow("Anmerkungen", self.input_notes)

        self.left_layout.addWidget(self.expanded_frame)

        # Button-Reihe
        self.buttons_row = QHBoxLayout()
        self.btn_expand = QPushButton("Erweitern")
        self.btn_appointment = QPushButton("Termin vergeben")
        self.btn_save = QPushButton("Speichern")
        self.btn_cancel = QPushButton("Abbrechen")
        self.buttons_row.addWidget(self.btn_expand)
        self.buttons_row.addStretch()
        self.buttons_row.addWidget(self.btn_appointment)
        self.buttons_row.addWidget(self.btn_save)
        self.buttons_row.addWidget(self.btn_cancel)

        self.left_layout.addLayout(self.buttons_row)
        self.left_layout.addStretch()

        # ------- Rechte Seite (Tabs)
        self.right = QWidget()
        self.right_layout = QVBoxLayout(self.right)
        self.tabs = QTabWidget()
        self.tabs.setObjectName("RightTabs")
        self.tabs.setTabsClosable(False)

        # Platzhalter-Tabs
        def _placeholder_tab(text: str) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.addWidget(QLabel(text))
            lay.addStretch()
            return w

        self.tab_complaints = _placeholder_tab("Hauptbeschwerden – (noch) Platzhalter")
        self.tab_medications = _placeholder_tab("Medikamente – (noch) Platzhalter")
        self.tab_diagnoses = _placeholder_tab("Diagnosen – (noch) Platzhalter")
        self.tab_anamnesis = _placeholder_tab("Anamnese – (noch) Platzhalter")
        self.tab_family = _placeholder_tab("Familienanamnese – (noch) Platzhalter")
        self.tab_lifestyle = _placeholder_tab("Lebensstil – (noch) Platzhalter")

        # Rechnungen-Tab mit Filterleiste + Tabelle
        self.tab_billing = QWidget()
        billing_layout = QVBoxLayout(self.tab_billing)
        filter_row = QHBoxLayout()
        self.filter_year = QComboBox()
        self.filter_month = QComboBox()
        self.filter_year.addItems(["2025", "2024", "2023"])  # später dynamisch aus DB
        self.filter_month.addItems(["Alle", "01", "02", "03", "04", "05", "06",
                                    "07", "08", "09", "10", "11", "12"])
        filter_row.addWidget(QLabel("Jahr:"))
        filter_row.addWidget(self.filter_year)
        filter_row.addSpacing(12)
        filter_row.addWidget(QLabel("Monat:"))
        filter_row.addWidget(self.filter_month)
        filter_row.addStretch()
        self.billing_table = QTableView()
        billing_layout.addLayout(filter_row)
        billing_layout.addWidget(self.billing_table)

        self.tabs.addTab(self.tab_complaints, "Hauptbeschwerden")
        self.tabs.addTab(self.tab_medications, "Medikamente")
        self.tabs.addTab(self.tab_diagnoses, "Diagnosen")
        self.tabs.addTab(self.tab_anamnesis, "Anamnese")
        self.tabs.addTab(self.tab_family, "Familienanamnese")
        self.tabs.addTab(self.tab_lifestyle, "Lebensstil")
        self.tabs.addTab(self.tab_billing, "Rechnungen")

        self.right_layout.addWidget(self.tabs)

        # Splitter bestücken
        self.splitter.addWidget(self.left)
        self.splitter.addWidget(self.right)

        # Kompaktmodus initial: rechte Seite verstecken
        self.right.setVisible(False)
        self.splitter.setSizes([1, 0])

        # Events
        self.btn_expand.clicked.connect(self.toggle_expand)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.on_save)
        self.btn_appointment.clicked.connect(self.on_appointment)

        # Vorbelegen bei Bearbeitung
        if self.patient is not None:
            self._load_patient()

        # Startgröße
        self.setMinimumWidth(520)
        self.resize(640, 440)

    # ---------------- Zustandswechsel ----------------
    def toggle_expand(self):
        self.is_expanded = not self.is_expanded
        self.expanded_frame.setVisible(self.is_expanded)
        self.right.setVisible(self.is_expanded)
        self.btn_expand.setText("Reduzieren" if self.is_expanded else "Erweitern")
        self.subtitle_label.setText(
            "Erweiterte Angaben & Dokumentation" if self.is_expanded else "Stammdaten (Name bis Ort)"
        )
        if self.is_expanded:
            self.resize(1120, 720)
            self.splitter.setSizes([5, 7])
        else:
            self.resize(640, 440)
            self.splitter.setSizes([1, 0])

    # ---------------- Daten laden ----------------
    def _load_patient(self):
        p = self.patient
        if not p:
            return
        self.input_firstname.setText(p.first_name or "")
        self.input_lastname.setText(p.last_name or "")
        self.input_street.setText(p.street or "")
        self.input_postal_code.setText(p.postal_code or "")
        self.input_city.setText(p.city or "")
        self.input_allergies.setPlainText(p.allergies or "")
        self.input_notes.setPlainText(p.notes or "")
        self.title_label.setText("Patientendaten bearbeiten")

    # ---------------- Validierung ----------------
    def _validate(self):
        errors = []

        def _mark_invalid(widget, ok: bool):
            widget.setProperty("invalid", not ok)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

        ln = self.input_lastname.text().strip()
        fn = self.input_firstname.text().strip()
        plz = self.input_postal_code.text().strip()
        city = self.input_city.text().strip()

        _mark_invalid(self.input_lastname, bool(ln))
        _mark_invalid(self.input_firstname, bool(fn))
        _mark_invalid(self.input_postal_code, plz.isdigit() and len(plz) in (4, 5))
        _mark_invalid(self.input_city, bool(city))

        if not ln:
            errors.append("Nachname ist erforderlich.")
        if not fn:
            errors.append("Vorname ist erforderlich.")
        if not (plz.isdigit() and len(plz) in (4, 5)):
            errors.append("PLZ ist ungültig (nur Ziffern, 4–5 Stellen).")
        if not city:
            errors.append("Ort ist erforderlich.")

        return errors

    # ---------------- Speichern ----------------
    def on_save(self):
        errors = self._validate()
        if errors:
            QMessageBox.warning(self, "Eingaben prüfen", "\n".join(errors))
            return

        p = self.patient or Patient()
        p.last_name = self.input_lastname.text().strip()
        p.first_name = self.input_firstname.text().strip()
        p.street = self.input_street.text().strip() or None
        p.postal_code = self.input_postal_code.text().strip()
        p.city = self.input_city.text().strip()
        p.allergies = self.input_allergies.toPlainText().strip() or None
        p.notes = self.input_notes.toPlainText().strip() or None

        try:
            if self.patient is None:
                self.session.add(p)
            self.session.commit()
            self.patient = p
            self.patient_saved.emit(p)
            self.accept()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Speicherfehler", f"Die Daten konnten nicht gespeichert werden:\n{e}")

    # ---------------- Termin vergeben (Platzhalter) ----------------
    def on_appointment(self):
        """
        Platzhalter: Im nächsten Schritt kann hier der Termin-Dialog geöffnet werden.
        Workflow:
        - Validieren + (falls neu) speichern
        - Danach Termin-Logik aufrufen (z. B. parent.open_appointment_dialog(patient))
        """
        errors = self._validate()
        if errors:
            QMessageBox.information(self, "Termin vergeben", "Bitte zuerst die Pflichtfelder ausfüllen, dann Termin vergeben.")
            return

        if self.patient is None:
            # Speichern versuchen
            self.on_save()
            if self.result() != QDialog.Accepted:
                return

        QMessageBox.information(self, "Termin vergeben", "Terminvergabe-Dialog folgt im nächsten Schritt.")
