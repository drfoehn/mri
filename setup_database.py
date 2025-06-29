import sqlite3
import json
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), 'mri.db')
JSON_PATH = os.path.join(os.path.dirname(__file__), 'MRI.json')

def get_section_from_chapter(chapter_text):
    """Leitet die Sektion aus dem Kapiteltext ab."""
    if not chapter_text or not isinstance(chapter_text, str):
        return None
    
    match = re.match(r"(\d+)", chapter_text)
    if not match:
        return None
        
    major_chapter = int(match.group(1))
    
    if major_chapter == 2:
        return "Biochemistry"
    elif major_chapter == 3:
        return "Haematology"
    elif major_chapter == 4:
        return "Immunology"
    elif major_chapter == 5:
        return "Microbiology"
    elif major_chapter == 6:
        return "Virology"
    else:
        return None

def setup_database():
    """Löscht die alte DB, erstellt die Tabellen und füllt sie mit Daten aus der JSON-Datei."""
    
    # 1. Alte DB-Datei löschen, falls vorhanden
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Alte Datenbank '{DB_PATH}' gelöscht.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 2. Tabellen erstellen
    cursor.execute('''
        CREATE TABLE entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ref TEXT,
            source TEXT,
            level_of_evidence TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL,
            lang TEXT NOT NULL,
            section TEXT,
            chapter TEXT,
            subsection TEXT,
            clinical_situation TEXT,
            recommendation TEXT,
            FOREIGN KEY (entry_id) REFERENCES entries (id),
            UNIQUE(entry_id, lang)
        )
    ''')
    print("Tabellen 'entries' und 'translations' erstellt.")

    # 3. JSON-Datei laden
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"{len(data)} Einträge aus '{JSON_PATH}' geladen.")

    # 4. Daten importieren
    for item in data:
        # Sprachunabhängige Daten in 'entries' einfügen
        cursor.execute(
            "INSERT INTO entries (ref, source, level_of_evidence) VALUES (?, ?, ?)",
            (item.get('ref'), item.get('source'), item.get('level_of_evidence'))
        )
        entry_id = cursor.lastrowid
        section = get_section_from_chapter(item.get('chapter'))
        cursor.execute(
            """
            INSERT INTO translations (
                entry_id, lang, section, chapter, subsection, clinical_situation, recommendation
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry_id,
                'en',
                section,
                item.get('chapter'),
                item.get('subsection'),
                item.get('clinical_situation'),
                item.get('recommendation')
            )
        )

    conn.commit()
    conn.close()

    print("Datenbank-Setup erfolgreich abgeschlossen!")

if __name__ == '__main__':
    setup_database() 