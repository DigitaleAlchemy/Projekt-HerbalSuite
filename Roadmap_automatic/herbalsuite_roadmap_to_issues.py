import requests

# 🔐 GitHub Personal Access Token hier einfügen
GITHUB_TOKEN = "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"

# 📁 Erweiterte Roadmap mit allen Fortschritten und Modulen
roadmap = [
    # GUI & Setup
    {
        "title": "GUI-Hauptfenster mit Navigation erstellen",
        "labels": ["gui", "high-priority", "milestone-demo", "in progress"],
        "status": "In Progress"
    },
    {
        "title": "GUI-Styling nach Mockup umsetzen",
        "labels": ["gui", "ui", "design", "todo"],
        "status": "To Do"
    },
    {
        "title": "Installer für Windows erstellen",
        "labels": ["release", "setup", "todo"],
        "status": "To Do"
    },
    {
        "title": "README.md vervollständigen",
        "labels": ["documentation", "todo"],
        "status": "To Do"
    },

    # Nextcloud & Netzwerk
    {
        "title": "Nextcloud-Integration vorbereiten",
        "labels": ["nextcloud", "network", "blocked"],
        "status": "Blocked"
    },
    {
        "title": "Lokaler Netzwerkabgleich implementieren",
        "labels": ["network", "backend", "todo"],
        "status": "To Do"
    },

    # Modulstruktur (9 Hauptmodule)
    {
        "title": "Modul Diagnostik & Dokumentation implementieren",
        "labels": ["diagnostik", "backend", "in progress"],
        "status": "In Progress"
    },
    {
        "title": "Modul Klassische Naturheilverfahren implementieren",
        "labels": ["klassische-verfahren", "backend", "todo"],
        "status": "To Do"
    },
    {
        "title": "Modul Pflanzen- & Substanztherapie implementieren",
        "labels": ["pflanzen-therapie", "backend", "todo"],
        "status": "To Do"
    },
    {
        "title": "Modul Manuelle & Körpertherapien implementieren",
        "labels": ["manuelle-therapien", "backend", "todo"],
        "status": "To Do"
    },
    {
        "title": "Modul Energetische & feinstoffliche Verfahren implementieren",
        "labels": ["energetik", "backend", "todo"],
        "status": "To Do"
    },
    {
        "title": "Modul Psychotherapie & Entspannung implementieren",
        "labels": ["psychotherapie", "backend", "todo"],
        "status": "To Do"
    },
    {
        "title": "Modul Ganzheitliche Heilsysteme implementieren",
        "labels": ["ganzheitliche-systeme", "backend", "todo"],
        "status": "To Do"
    },
    {
        "title": "Modul Physikalische Therapien implementieren",
        "labels": ["physikalische-therapien", "backend", "todo"],
        "status": "To Do"
    },
    {
        "title": "Modul Verwaltung & Organisation implementieren",
        "labels": ["verwaltung", "backend", "todo"],
        "status": "To Do"
    }
]

# 📦 GitHub-Repository-Details
owner = "DigitaleAlchemy"
repo = "Projekt-HerbalSuite"
api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"

# 🔧 Header für Authentifizierung
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# 🧠 Hilfsfunktion: Alle bestehenden Issues abrufen
def get_existing_issues():
    issues = []
    page = 1
    while True:
        response = requests.get(f"{api_url}?state=all&page={page}", headers=headers)
        if response.status_code != 200:
            print("❌ Fehler beim Abrufen der bestehenden Issues.")
            break
        data = response.json()
        if not data:
            break
        issues.extend(data)
        page += 1
    return issues

# 📝 Roadmap synchronisieren
existing_issues = get_existing_issues()
existing_titles = {issue["title"]: issue for issue in existing_issues}

for item in roadmap:
    title = item.get("title", "Kein Titel")
    labels = item.get("labels", [])
    status = item.get("status", "Unbekannt")
    body = f"Status: {status}"

    if title in existing_titles:
        # 🔄 Issue existiert – aktualisieren
        issue_number = existing_titles[title]["number"]
        update_url = f"{api_url}/{issue_number}"
        update_data = {
            "body": body,
            "labels": labels
        }
        response = requests.patch(update_url, headers=headers, json=update_data)
        if response.status_code == 200:
            print(f"🔄 Issue aktualisiert: {title}")
        else:
            print(f"❌ Fehler beim Aktualisieren von Issue: {title}")
            print(f"Antwort: {response.status_code} - {response.text}")
    else:
        # 🆕 Neues Issue erstellen
        issue_data = {
            "title": title,
            "body": body,
            "labels": labels
        }
        response = requests.post(api_url, headers=headers, json=issue_data)
        if response.status_code == 201:
            print(f"✅ Neues Issue erstellt: {title}")
        else:
            print(f"❌ Fehler beim Erstellen von Issue: {title}")
            print(f"Antwort: {response.status_code} - {response.text}")
