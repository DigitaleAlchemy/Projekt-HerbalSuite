# HerbalSuite

Modulare Praxissoftware für Heilpraktiker – mit lokalem Datenspeicher, optionalem LAN‑Sync und geplanter Nextcloud‑Integration.

> **Projektstatus:** Konzeption & frühes Prototyping (laufend). 

---

## 🎯 Ziel & Leitbild
HerbalSuite soll eine **lokal installierbare Windows‑Anwendung (Windows 10/11)** werden, entwickelt in **Python**. 
Daten werden **lokal** gespeichert; bei mehreren Nutzer:innen ist ein **Abgleich im lokalen Netzwerk** vorgesehen. Eine **optionale, sichere Nextcloud‑Anbindung** ist geplant. Das Grundsystem ist für alle Heilpraktiker nutzbar; zusätzliche **Module** lassen sich je nach Spezialisierung aktivieren. Ein Schwerpunkt liegt auf einer **grafisch außergewöhnlichen UI**, die sich klar von Standardsoftware abhebt.

---

## 🧩 Modulübersicht (geplant)
1. **Diagnostik & Dokumentation**
2. **Klassische Naturheilverfahren**
3. **Pflanzen- & Substanztherapie**
4. **Manuelle & Körpertherapien**
5. **Energetische & feinstoffliche Verfahren**
6. **Psychotherapie & Entspannung**
7. **Ganzheitliche Heilsysteme**
8. **Physikalische Therapien**
9. **Verwaltung & Organisation**

> *Hinweis:* Das **Grundsystem** deckt allgemeine Praxisfunktionen ab; **Zusatzmodule** können gezielt aktiviert werden.

---

## 🏗️ Architektur (geplant)
- **Plattform:** Windows 10/11 (lokale Installation)
- **Technologie:** Python (UI‑Framework TBD; z. B. Qt/PySide6 oder alternativ Kivy)
- **Datenhaltung:** lokal (Datei‑/DB‑basiert), optionale **LAN‑Synchronisation**
- **Cloud‑Option:** optionale, sichere **Nextcloud‑Integration** (z. B. verschlüsselte Datei‑Syncs)
- **Erweiterbarkeit:** modulare Architektur mit aktivierbaren Komponenten
- **Design:** visuell eigenständige, moderne Oberfläche; Orientierung am geplanten UI‑Mockup

---

## ✨ Geplante Kernfunktionen
- Mandanten‑ und Patientenverwaltung
- Dokumentation & Anamnese
- Terminplanung & Kalender
- Abrechnung/Verwaltung (später)
- Modulverwaltung (Aktivierung/Deaktivierung)
- Datensicherung, Export/Import

---

## 🚀 Schnellstart (Entwicklung)
> *Die folgenden Schritte skizzieren den lokalen Entwicklungs‑Setup. Details (z. B. konkrete Paketabhängigkeiten) folgen, sobald erste Codeartefakte vorliegen.*

```powershell
# Repository klonen
git clone https://github.com/DigitaleAlchemy/Projekt-HerbalSuite.git
cd Projekt-HerbalSuite

# (Optional) Python‑Virtuelle Umgebung
python -m venv .venv
. .venv/Scripts/Activate.ps1  # PowerShell

# Abhängigkeiten installieren (falls requirements.txt vorhanden)
pip install -r requirements.txt

# Start eines Prototyps / Dev‑Skripts (sobald verfügbar)
python app.py
