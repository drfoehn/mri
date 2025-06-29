import sqlite3
import json

DB_PATH = 'mri.db'
JSON_PATH = 'other_docs/german.json'

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(JSON_PATH, encoding='utf-8') as f:
    data = json.load(f)

for entry in data:
    cur.execute("""
        INSERT OR IGNORE INTO translations
        (entry_id, lang, section, chapter, subsection, clinical_situation, recommendation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        entry.get('entry_id'),
        entry.get('lang', 'de'),
        entry.get('section'),
        entry.get('chapter'),
        entry.get('subsection'),
        entry.get('clinical_situation'),
        entry.get('recommendation')
    ))

conn.commit()
conn.close()
print("Import abgeschlossen!")
