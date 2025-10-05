import json
import re

# JSON-Datei laden
with open('MRI_en_de.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Funktion zum Korrigieren der Referenz-Links
def fix_reference_links(source):
    if not source:
        return source
    
    # Pattern für Referenznummern am Ende: Jahr.Referenznummer
    # Beispiele: "2010.6" -> Link zu Referenz #6
    #           "2019.8" -> Link zu Referenz #8
    
    def replace_reference(match):
        prefix = match.group(1)  # Komma oder Leerzeichen vor der Nummer
        ref_year_dot_num = match.group(2)  # Die Referenznummer (z.B. "2010.6")
        
        # Extrahiere die Referenznummer nach dem Punkt
        ref_number = ref_year_dot_num.split('.')[1]  # "2010.6" -> "6"
        
        return f'{prefix}<a href="/references#ref-{ref_number}" target="_blank" class="reference-link">{ref_year_dot_num}<sup>ref</sup></a>'
    
    # Pattern: [,\s](\d{4}\.\d+)(?:\s*)$
    pattern = r'([,\s])(\d{4}\.\d+)(?:\s*)$'
    enhanced = re.sub(pattern, replace_reference, source)
    
    return enhanced

# Alle Einträge korrigieren
for entry in data:
    if 'source' in entry:
        entry['source'] = fix_reference_links(entry['source'])

# Backup erstellen
with open('MRI_en_de_backup_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Korrigierte Datei speichern
with open('MRI_en_de.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Referenz-Links erfolgreich korrigiert!")
print("Backup erstellt als: MRI_en_de_backup_fixed.json")

# Zeige einige Beispiele
print("\nBeispiele der Korrekturen:")
examples = 0
for entry in data[:20]:  # Erste 20 Einträge prüfen
    if 'source' in entry and re.search(r'\d{4}\.\d+', entry['source']):
        if examples < 3:  # Zeige nur 3 Beispiele
            print(f"  {entry['source']}")
            examples += 1
