import re

# References HTML-Datei lesen
with open('templates/references.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern für Referenzzeilen finden und IDs hinzufügen
def add_anchor_ids(match):
    ref_number = match.group(1)
    rest_of_line = match.group(2)
    return f'<tr id="ref-{ref_number}"><td><strong>{ref_number}</strong></td><td>{rest_of_line}</td></tr>'

# Pattern: <tr><td><strong>1</strong></td><td>...</td></tr>
pattern = r'<tr><td><strong>(\d+)</strong></td><td>(.*?)</td></tr>'
content = re.sub(pattern, add_anchor_ids, content, flags=re.DOTALL)

# Backup erstellen
with open('templates/references_backup.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Aktualisierte Datei speichern
with open('templates/references.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Referenz-Anker erfolgreich hinzugefügt!")
print("Backup erstellt als: templates/references_backup.html")
