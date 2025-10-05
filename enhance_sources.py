import json
import re

# JSON-Datei laden
with open('MRI_en_de.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Funktion zum Verbessern der Source-Spalte mit Referenz-Links
def enhance_source(source):
    if not source:
        return source
    
    # Pattern für Referenznummern am Ende: Zahl nach Punkt oder Komma
    # Beispiele: "NICE Clinical Knowledge Summary, 2019.8" -> "2019.8"
    #           "GAIN, 2015.9" -> "2015.9"
    
    # Finde Referenznummern am Ende der Source
    pattern = r'([,\s])(\d{4}\.\d+)(?:\s*)$'
    
    def replace_reference(match):
        prefix = match.group(1)  # Komma oder Leerzeichen vor der Nummer
        ref_num = match.group(2)  # Die Referenznummer (z.B. "2019.8")
        
        # Erstelle Link zur References-Seite mit Anker zur Referenznummer
        # Die Referenznummer entspricht der Nummer in der References-Tabelle
        ref_number = int(float(ref_num))  # "2019.8" -> 2019
        
        return f'{prefix}<a href="/references#ref-{ref_number}" target="_blank" class="reference-link">{ref_num}<sup>ref</sup></a>'
    
    enhanced = re.sub(pattern, replace_reference, source)
    
    return enhanced

# Alle Einträge verbessern
for entry in data:
    if 'source' in entry:
        entry['source'] = enhance_source(entry['source'])

# Backup erstellen
with open('MRI_en_de_backup_enhanced.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Verbesserte Datei speichern
with open('MRI_en_de.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Source-Spalten erfolgreich mit Referenz-Links verbessert!")
print("Backup erstellt als: MRI_en_de_backup_enhanced.json")

# Zeige einige Beispiele
print("\nBeispiele der Verbesserungen:")
examples = 0
for entry in data[:20]:  # Erste 20 Einträge prüfen
    if 'source' in entry and re.search(r'\d{4}\.\d+', entry['source']):
        if examples < 3:  # Zeige nur 3 Beispiele
            print(f"  {entry['source']}")
            examples += 1
