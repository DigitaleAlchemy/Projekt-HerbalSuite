
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Text
from .db import Base

class Patient(Base):
    __tablename__ = 'patients'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_name: Mapped[str] = mapped_column(String(120), index=True)
    first_name: Mapped[str] = mapped_column(String(120), index=True)
    birth_date: Mapped[Date | None]
    encounters: Mapped[list['Encounter']] = relationship(back_populates='patient')

class Encounter(Base):
    __tablename__ = 'encounters'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'), index=True)
    when: Mapped[DateTime]
    reason: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[list['Note']] = relationship(back_populates='encounter')
    patient: Mapped['Patient'] = relationship(back_populates='encounters')

class Note(Base):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    encounter_id: Mapped[int] = mapped_column(ForeignKey('encounters.id'), index=True)
    soap_subjective: Mapped[str | None] = mapped_column(Text)
    soap_objective: Mapped[str | None] = mapped_column(Text)
    soap_assessment: Mapped[str | None] = mapped_column(Text)
    soap_plan: Mapped[str | None] = mapped_column(Text)
    encounter: Mapped['Encounter'] = relationship(back_populates='notes')

class Document(Base):
    __tablename__ = 'documents'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'), index=True)
    title: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(1024))

class Herb(Base):
    __tablename__ = 'herbs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

class Recipe(Base):
    __tablename__ = 'recipes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    text: Mapped[str | None] = mapped_column(Text)

class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(120), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
