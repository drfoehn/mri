import json
import re

# JSON-Datei laden
with open('MRI_en_de.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Funktion zum Korrigieren der Referenz-Links
def fix_reference_links(source):
    if not source:
        return source
    
    # Finde alle Links mit falschen Referenznummern und korrigiere sie
    # Pattern: href="/references#ref-(\d{4})" -> href="/references#ref-(\d+)"
    
    def replace_link(match):
        full_match = match.group(0)
        year = match.group(1)  # Das Jahr aus dem Link (z.B. "2010")
        
        # Finde die Referenznummer nach dem Jahr im Text
        ref_pattern = rf'{year}\.(\d+)'
        ref_match = re.search(ref_pattern, source)
        
        if ref_match:
            ref_number = ref_match.group(1)  # Die tatsächliche Referenznummer
            return full_match.replace(f'ref-{year}', f'ref-{ref_number}')
        
        return full_match
    
    # Pattern für Links: href="/references#ref-(\d{4})"
    pattern = r'href="/references#ref-(\d{4})"'
    corrected = re.sub(pattern, replace_link, source)
    
    return corrected

# Alle Einträge korrigieren
for entry in data:
    if 'source' in entry:
        entry['source'] = fix_reference_links(entry['source'])

# Backup erstellen
with open('MRI_en_de_backup_fixed_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Korrigierte Datei speichern
with open('MRI_en_de.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Referenz-Links erfolgreich korrigiert!")
print("Backup erstellt als: MRI_en_de_backup_fixed_v2.json")

# Zeige einige Beispiele
print("\nBeispiele der Korrekturen:")
examples = 0
for entry in data[:20]:  # Erste 20 Einträge prüfen
    if 'source' in entry and 'ref-20' in entry['source']:
        if examples < 3:  # Zeige nur 3 Beispiele
            print(f"  {entry['source']}")
            examples += 1
