# 🗺️ HerbalSuite Roadmap

Modulare Praxissoftware für Heilpraktiker – mit lokalem Datenspeicher, optionalem LAN‑Sync und geplanter Nextcloud‑Integration.

---

## 🎯 Projektziel

HerbalSuite soll eine **lokal installierbare Windows‑Anwendung (Windows 10/11)** werden, entwickelt in **Python**.  
Daten werden **lokal** gespeichert; bei mehreren Nutzer:innen ist ein **Abgleich im lokalen Netzwerk** vorgesehen.  
Eine **optionale, sichere Nextcloud‑Anbindung** ist geplant.  
Ein Schwerpunkt liegt auf einer **grafisch außergewöhnlichen UI**, die sich klar von Standardsoftware abhebt.

---

## 📋 Kanban-Board Struktur

Das GitHub Project Board ist in folgende Spalten unterteilt:

- 🕘 **Backlog** – geplante Aufgaben
- 🔧 **In Arbeit** – aktuell bearbeitet
- 🔍 **Review** – wartet auf Code-Review/Test
- ✅ **Done** – abgeschlossen

---

## 📌 Roadmap-Tabelle

| 🔢 Nr. | 🧩 Titel | 🗂️ Kategorie | ⚡ Priorität | 📌 Status |
|-------|---------|--------------|-------------|-----------|
| 1 | EPIC: UI‑Mockup in klickbare Oberfläche übertragen | epic, ui | P1 | Backlog |
| 2 | Projektgrundgerüst: /src-Struktur, Packaging, Config, Logging | task, infra | P1 | Backlog |
| 3 | Designsystem & Theme (Farben, Typografie, Komponenten-Baukasten) | feature, ui | P2 | Backlog |
| 4 | Navigation & Layout-Router | feature, ui | P2 | Backlog |
| 5 | Datenmodell & Persistenz: lokale DB (SQLite + ORM) | feature, backend | P1 | Backlog |
| 6 | Modul-System: Laden/Aktivieren/Deaktivieren (Plugin-Architektur) | feature, backend | P1 | Backlog |
| 7 | Patientenverwaltung (CRUD, Validierung, Suche) | feature, ui, backend | P2 | Backlog |
| 8 | Anamnese & Dokumentation: Formular-Engine + Vorlagen | feature, ui, backend | P2 | Backlog |
| 9 | Terminplanung & Kalender (Basis) | feature, ui | P2 | Backlog |
| 10 | Backup/Export + LAN‑Sync: Konzept & Prototyp | feature, security, backend | P2 | Backlog |
| 11 | Nextcloud-Integration (optional): Evaluierung & Sicherheitskonzept | task, infra, security | P2 | Backlog |
| 12 | CI-Basis: Lint, Format, Tests + GitHub Actions | infra, docs | P2 | Backlog |
| 13 | Windows‑Installer: Packaging (PyInstaller/Briefcase) + Signierung | infra | P2 | Backlog |
| 14 | Datenschutz & Sicherheit: Leitlinien dokumentieren | docs, security | P2 | Backlog |
| 15 | Lizenz festlegen & LICENSE hinzufügen | docs | P2 | Backlog |

---

## 🔗 GitHub Project Board

👉 Alle Aufgaben sind im GitHub Project Board organisiert:  
🔗 [HerbalSuite Roadmap Board](https://github.com/users/DigitaleAlchemy/projects)

Du kannst dort Aufgaben verschieben, bearbeiten und mit Pull Requests verknüpfen.

---

📁 Diese Datei wird regelmäßig aktualisiert und dient als zentrale Übersicht für die Projektentwicklung.
