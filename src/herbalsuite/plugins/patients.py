# -*- coding: utf-8 -*-
from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QTableView, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt

# Registry-Dekorator wie gehabt
from . import register

# Session-Helper: bevorzugt get_session, sonst kleiner Fallback
try:
    from herbalsuite.data.db import get_session  # type: ignore
except Exception:
    from sqlalchemy.orm import sessionmaker
    from herbalsuite.data.db import engine  # type: ignore
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    def get_session():  # type: ignore
        return SessionLocal()

from herbalsuite.data.models import Patient
from herbalsuite.ui.patient_dialog import PatientDialog
from herbalsuite.ui.patient_table_model import PatientTableModel


@register("patients")
def make(parent=None):
    w = QWidget(parent)
    layout = QVBoxLayout(w)
    layout.addWidget(QLabel("Patientenverwaltung (MVP)"))

    # Toolbar
    toolbar = QHBoxLayout()
    btn_new = QPushButton("Neu")
    btn_edit = QPushButton("Bearbeiten")
    search_edit = QLineEdit()
    search_edit.setPlaceholderText("Suchen (Name/Ort/E‑Mail)…")
    toolbar.addWidget(btn_new)
    toolbar.addWidget(btn_edit)
    toolbar.addStretch(1)
    toolbar.addWidget(search_edit)
    layout.addLayout(toolbar)

    # Tabelle
    table = QTableView()
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setAlternatingRowColors(True)
    layout.addWidget(table)

    # Session-Lebenszyklus am Widget hängen
    session = get_session()
    w.destroyed.connect(lambda *_: session.close())

    # Model
    model = PatientTableModel([])
    table.setModel(model)

    # Daten laden (mit Suche)
    def load():
        from sqlalchemy import or_

        q = session.query(Patient)
        s = search_edit.text().strip()
        if s:
            like = f"%{s}%"
            patients = (
                q.filter(
                    or_(
                        Patient.last_name.ilike(like),
                        Patient.first_name.ilike(like),
                        Patient.city.ilike(like),
                        Patient.email.ilike(like),
                    )
                )
                .order_by(Patient.last_name, Patient.first_name)
                .all()
            )
        else:
            patients = q.order_by(Patient.last_name, Patient.first_name).all()
        model.setPatients(patients)

    # Aktionen
    def add_patient():
        dlg = PatientDialog(session, parent=w)
        if dlg.exec():
            load()

    def edit_patient():
        idx = table.currentIndex()
        if not idx.isValid():
            QMessageBox.information(w, "Bearbeiten", "Bitte zuerst einen Patienten auswählen.")
            return
        p = model.patient_at(idx.row())
        dlg = PatientDialog(session, patient=p, parent=w)
        if dlg.exec():
            load()

    # Signals
    btn_new.clicked.connect(add_patient)
    btn_edit.clicked.connect(edit_patient)
    search_edit.textChanged.connect(lambda _text: load())

    # initial laden
    load()
    return w
