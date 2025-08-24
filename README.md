HerbalSuite – Praxissoftware für Heilpraktiker (GNUmed‑inspiriert)
Minimal lauffähiges Grundgerüst in Python 3.10+ mit PySide6 (UI) und SQLAlchemy (Datenzugriff) für Windows 10/11.
Keine Übernahme von GNUmed‑Code; nur fachliche Ideen (EMR, Patient, Encounter, Dokumente) werden aufgegriffen.

Features (MVP)
Startfenster in Deutsch mit Seitenleiste: Startseite, Patienten, Rezepturen, Diagnostik, Lagerverwaltung, Einstellungen
Patientenverwaltung mit Suchfunktion, Neu/Bearbeiten-Dialog, Doppelklick-Handler
Kompakter Patientendialog mit Tabs (Stammdaten, Kontakt, Anamnese)
Erweitertes Datenmodell (Geburtsdatum, Kontakt, Anamnese, Indikator „Offene Rechnung“)
Plugin‑fähige Navigation (einfache Registry)
SQLite-Datenbank als Standard (PostgreSQL optional vorbereitet)
Konfigurierbarer Dokumentenpfad (z. B. Nextcloud‑Sync‑Ordner)
Roadmap-Sync-Skript für GitHub-Issues (scripts/herbalsuite_roadmap_to_issues.py)
