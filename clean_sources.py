import json
import re

# JSON-Datei laden
with open('MRI_en_de.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Funktion zum Bereinigen der Source-Spalte
def clean_source(source):
    if not source:
        return source
    
    # Entferne Level of Evidence-Informationen in eckigen Klammern
    # Pattern: [Level of evidence – X.] oder [Level of evidence –\nX.]
    cleaned = re.sub(r'\[Level of evidence[^]]*\]', '', source, flags=re.IGNORECASE | re.DOTALL)
    
    # Bereinige überflüssige Zeilenumbrüche und Leerzeichen
    cleaned = re.sub(r'\n+', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned

# Alle Einträge bereinigen
for entry in data:
    if 'source' in entry:
        entry['source'] = clean_source(entry['source'])

# Backup erstellen
with open('MRI_en_de_backup_clean.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Bereinigte Datei speichern
with open('MRI_en_de.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Source-Spalten erfolgreich bereinigt!")
print("Backup erstellt als: MRI_en_de_backup_clean.json")
