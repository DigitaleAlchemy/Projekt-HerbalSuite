
# -*- coding: utf-8 -*-
"""SQLAlchemy-Modelle für HerbalSuite (erweitert).

Erweitert das Patient-Modell um:
- Geburtsdatum, Geschlecht
- Kontaktdaten (Telefon, Mobil, E‑Mail, Straße, PLZ, Ort)
- Anamnese-Felder
- Indikator has_open_invoice
"""
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, Index
from .db import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name  = Column(String(100), nullable=False)

    date_of_birth = Column(Date, nullable=True)
    # 'm' = männlich, 'w' = weiblich, 'd' = divers, 'x' = ohne Angabe, 'u' = unbekannt
    sex = Column(String(1), nullable=True)

    phone = Column(String(50), nullable=True)
    mobile = Column(String(50), nullable=True)
    email  = Column(String(255), nullable=True)

    street      = Column(String(255), nullable=True)
    postal_code = Column(String(20),  nullable=True)
    city        = Column(String(100), nullable=True)

    # Anamnese-Felder
    chief_complaint = Column(Text, nullable=True)   # Hauptbeschwerde
    allergies       = Column(Text, nullable=True)
    medications     = Column(Text, nullable=True)
    diagnoses       = Column(Text, nullable=True)
    family_history  = Column(Text, nullable=True)
    lifestyle       = Column(Text, nullable=True)
    notes           = Column(Text, nullable=True)

    # Rechnungs-Indikator
    has_open_invoice = Column(Boolean, nullable=False, server_default="0", default=False)

# Indizes
Index("idx_patients_name", Patient.last_name, Patient.first_name)
Index("idx_patients_dob", Patient.date_of_birth)
