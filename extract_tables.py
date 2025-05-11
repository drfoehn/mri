import pdfplumber
import pandas as pd
import re
import json

# Pfad zur PDF-Datei
PDF_PATH = "other_docs/MRI.pdf"
# Name der Ausgabedatei
OUTPUT_JSON = "MRI.json"

# Mapping Ref-Präfix zu Kapitel
REF_PREFIX_TO_CHAPTER = {
    "B-R": "2.1 Renal (refers to the measurement of U&E, unless otherwise stated)",
    "B-B": "2.2 Bone (refers to the measurement of the bone profile, unless otherwise stated)",
    "B-L": "2.3 Liver (refers to the measurement of LFTs, unless otherwise stated)",
    "B-LP": "2.4 Lipids (refers to the measurement of lipid profile [non-fasting], unless otherwise stated)",
    "B-E": "2.5 Endocrine related (for pregnancy-related endocrinology, see 2.12)",
    "B-C": "2.6 Cardiac",
    "B-G": "2.7 Gastrointestinal",
    "B-SP": "2.8 Specific proteins",
    "B-TM": "2.9 Tumour markers",
    "B-TD": "2.10 Therapeutic drug monitoring",
    "B-O": "2.11 Occupational/toxicology",
    "B-P": "2.12 Pregnancy related",
    "B-CH": "2.13 Paediatric related",
    "H-FBC": "3.1 Haematology general",
    "H-CS": "3.2 Haematology coagulation",
    "H-BGAS": "3.3 Haematology transfusion (general and screening group in PBLC)",
    "I-": "4 Immunology recommendations",
    "M-": "5.1 General microbiology",
    "V-": "6.1 Congenital/perinatal blood-borne viral infection – testing in asymptomatic infants",
    # ggf. weitere Zuordnungen ergänzen
}

# Hilfsfunktion, um Level of evidence aus Source zu extrahieren
def extract_level_of_evidence(source):
    if not isinstance(source, str):
        return ""
    match = re.search(r"Level of evidence\s*[–-]\s*([A-Za-z0-9+]+)", source)
    if match:
        return match.group(1)
    return ""

def extract_ref_prefix(ref):
    if not isinstance(ref, str):
        return None
    match = re.match(r"([A-Z-]+)", ref)
    if match:
        return match.group(1)
    return None

def is_subsection_row(row_dict):
    # Eine Subsection hat meist nur in der ersten Spalte Text, die anderen sind leer
    ref = (str(row_dict.get('ref', '')) or '').strip()
    clinical = (str(row_dict.get('clinical situation', '')) or '').strip()
    recommendation = (str(row_dict.get('recommendation', '')) or '').strip()
    source = (str(row_dict.get('source', '')) or '').strip()
    if ref and not clinical and not recommendation and not source:
        return True
    return False

# Daten sammeln
all_entries = []

with pdfplumber.open(PDF_PATH) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        current_subsection = None
        for table in tables:
            if not table or len(table) < 2:
                continue
            header = [h.strip().lower() if h else '' for h in table[0]]
            # Akzeptiere Tabellen mit 'ref' und entweder 'clinical situation' oder 'test'
            if 'ref' in header and ('clinical situation' in header or 'test' in header):
                for row in table[1:]:
                    row_dict = dict(zip(header, row))
                    # Subsection erkennen
                    if is_subsection_row(row_dict):
                        current_subsection = (str(row_dict.get('ref', '')) or '').strip()
                        continue
                    ref = (str(row_dict.get('ref', '')) or '').strip()
                    ref_prefix = extract_ref_prefix(ref)
                    chapter = REF_PREFIX_TO_CHAPTER.get(ref_prefix, None)
                    # Fallback: falls kein Kapitel gefunden, Immunologie zuordnen, wenn Ref mit I- beginnt
                    if not chapter and ref.startswith('I-'):
                        chapter = REF_PREFIX_TO_CHAPTER.get('I-', '4 Immunology recommendations')
                    # clinical_situation aus passender Spalte holen
                    if 'clinical situation' in header:
                        clinical_situation = (str(row_dict.get('clinical situation', '')) or '').strip()
                    elif 'test' in header:
                        clinical_situation = (str(row_dict.get('test', '')) or '').strip()
                    else:
                        clinical_situation = ''
                    entry = {
                        "chapter": chapter,
                        "subsection": current_subsection,
                        "ref": ref,
                        "clinical_situation": clinical_situation,
                        "recommendation": (str(row_dict.get('recommendation', '')) or '').strip(),
                        "source": (str(row_dict.get('source', '')) or '').strip(),
                    }
                    entry["level_of_evidence"] = extract_level_of_evidence(entry["source"])
                    all_entries.append(entry)

# Speichere als JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(all_entries, f, ensure_ascii=False, indent=2)

print(f"Fertig! {len(all_entries)} Einträge gespeichert in {OUTPUT_JSON}") 