
# -*- coding: utf-8 -*-
"""Idempotente Migration für Patiententabelle (SQLite & Postgres).

Verwendung:
    from herbalsuite.data.migrate import migrate_patients
    migrate_patients()
"""
from sqlalchemy import text
from .db import engine

COLUMNS = [
    ("date_of_birth",    "DATE"),
    ("sex",              "VARCHAR(1)"),
    ("phone",            "VARCHAR(50)"),
    ("mobile",           "VARCHAR(50)"),
    ("email",            "VARCHAR(255)"),
    ("street",           "VARCHAR(255)"),
    ("postal_code",      "VARCHAR(20)"),
    ("city",             "VARCHAR(100)"),
    ("chief_complaint",  "TEXT"),
    ("allergies",        "TEXT"),
    ("medications",      "TEXT"),
    ("diagnoses",        "TEXT"),
    ("family_history",   "TEXT"),
    ("lifestyle",        "TEXT"),
    ("notes",            "TEXT"),
    ("has_open_invoice", "BOOLEAN NOT NULL DEFAULT 0"),
]

def migrate_patients():
    dialect = engine.dialect.name
    with engine.begin() as conn:
        if dialect == 'sqlite':
            existing = {row[1] for row in conn.execute(text("PRAGMA table_info(patients)")).fetchall()}
            for col, ddl in COLUMNS:
                if col not in existing:
                    conn.execute(text(f"ALTER TABLE patients ADD COLUMN {col} {ddl}"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(last_name, first_name)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_patients_dob ON patients(date_of_birth)"))
        elif dialect in ('postgresql', 'postgres'):
            for col, ddl in COLUMNS:
                conn.execute(text(f"ALTER TABLE patients ADD COLUMN IF NOT EXISTS {col} {ddl}"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(last_name, first_name)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_patients_dob ON patients(date_of_birth)"))
        else:
            # generischer Fallback
            for col, ddl in COLUMNS:
                try:
                    conn.execute(text(f"ALTER TABLE patients ADD COLUMN IF NOT EXISTS {col} {ddl}"))
                except Exception:
                    pass

if __name__ == '__main__':
    migrate_patients()
    print("Migration abgeschlossen.")
