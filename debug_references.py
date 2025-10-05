import json

# JSON-Datei laden und Referenznummern analysieren
with open('MRI_en_de.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Analysiere Referenznummern in der Source-Spalte:")
reference_numbers = set()

for entry in data:
    if 'source' in entry and entry['source']:
        import re
        # Finde alle Referenznummern in der Source
        matches = re.findall(r'(\d{4}\.\d+)', entry['source'])
        for match in matches:
            reference_numbers.add(match)

print("Gefundene Referenznummern:", sorted(reference_numbers))

# Prüfe die ersten paar Einträge
print("\nErste 5 Einträge mit Referenznummern:")
count = 0
for entry in data:
    if 'source' in entry and entry['source'] and '2010.6' in entry['source']:
        print(f"Source: {entry['source']}")
        count += 1
        if count >= 3:
            break
