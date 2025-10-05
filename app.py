from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from markupsafe import Markup
import re
from flask_babel import Babel, _

app = Flask(__name__)
# IMPORTANT: Change this secret key for production!
app.secret_key = 'a-super-secret-key-that-you-should-change'

# --- Babel Configuration ---
app.config['LANGUAGES'] = {
    'en': 'English',
    'de': 'German'
}

def get_locale():
    # 1. Check for language in session (user's explicit choice)
    if 'language' in session:
        return session['language']
    # 2. Use the best match from the user's browser languages.
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel = Babel(app, locale_selector=get_locale)

@app.route('/set-language/<language>')
def set_language(language=None):
    session['language'] = language
    # Redirect to the previous page or homepage
    return redirect(request.referrer or url_for('index'))
# --- End Babel Configuration ---

# JSON laden
DATA_PATH = os.path.join(os.path.dirname(__file__), 'MRI_en_de.json')
with open(DATA_PATH, encoding='utf-8') as f:
    data = json.load(f)

# Hilfsfunktionen für Sprachfilterung
def get_data_for_language(lang):
    """Gibt nur die Daten für die gewählte Sprache zurück"""
    return [entry for entry in data if entry.get('lang') == lang]

def get_sections_for_language(lang):
    """Gibt die Sections für die gewählte Sprache zurück"""
    lang_data = get_data_for_language(lang)
    return sorted(set(entry.get('section', '') for entry in lang_data if entry.get('section', '')))

def get_chapters_for_language(lang):
    """Gibt die Chapters für die gewählte Sprache zurück"""
    lang_data = get_data_for_language(lang)
    return sorted(set(entry['chapter'] for entry in lang_data if entry['chapter']))

def get_subsections_for_language(lang):
    """Gibt die Subsections für die gewählte Sprache zurück"""
    lang_data = get_data_for_language(lang)
    return sorted(set(entry['subsection'] for entry in lang_data if entry['subsection']))

@app.route('/', methods=['GET', 'POST'])
def index():
    # Aktuelle Sprache aus Session oder Browser-Präferenz
    current_lang = session.get('language', get_locale())
    
    # Daten für die aktuelle Sprache laden
    lang_data = get_data_for_language(current_lang)
    sections = get_sections_for_language(current_lang)
    chapters = get_chapters_for_language(current_lang)
    subsections = get_subsections_for_language(current_lang)
    
    results = []
    selected_section = request.form.get('section') if request.method == 'POST' else ''
    selected_chapter = request.form.get('chapter') if request.method == 'POST' else ''
    selected_subsection = request.form.get('subsection') if request.method == 'POST' else ''
    search_text = request.form.get('search_text', '').strip() if request.method == 'POST' else ''

    # Bei GET-Request alle Einträge für die aktuelle Sprache anzeigen
    if request.method == 'GET':
        results = lang_data
    elif request.method == 'POST' and (selected_section or selected_chapter or selected_subsection or search_text):
        # Filterung auf die aktuelle Sprache beschränken
        filtered_results = [entry for entry in lang_data
                   if (not selected_section or entry.get('section', '') == selected_section)
                   and (not selected_chapter or entry.get('chapter', '') == selected_chapter)
                   and (not selected_subsection or entry.get('subsection', '') == selected_subsection)
                   and (not search_text or re.search(search_text, entry['clinical_situation'], re.IGNORECASE))]
        
        if search_text:
            for entry in filtered_results:
                # Create a copy to avoid modifying the original data
                new_entry = entry.copy()
                # Highlight the search term
                new_entry['clinical_situation'] = re.sub(f'({re.escape(search_text)})', r'<mark>\1</mark>', new_entry['clinical_situation'], flags=re.IGNORECASE)
                results.append(new_entry)
        else:
            results = filtered_results

    # Mark HTML in source field as safe
    for entry in results:
        if 'source' in entry and entry['source']:
            entry['source'] = Markup(entry['source'])
    
    return render_template('index.html',
                           sections=sections,
                           chapters=chapters,
                           subsections=subsections,
                           results=results,
                           selected_section=selected_section,
                           selected_chapter=selected_chapter,
                           selected_subsection=selected_subsection,
                           search_text=search_text,
                           current_lang=current_lang)

@app.route('/get_chapters', methods=['POST'])
def get_chapters():
    section = request.form.get('section', '')
    current_lang = session.get('language', get_locale())
    lang_data = get_data_for_language(current_lang)
    
    filtered_chapters = sorted(set(entry['chapter'] for entry in lang_data if entry.get('section', '') == section and entry['chapter']))
    options = '<option value="">Alle</option>' + ''.join(f'<option value="{c}">{c}</option>' for c in filtered_chapters)
    select_html = f'''
    <select class="form-select" id="chapter" name="chapter"
            hx-post="/get_subsections" hx-trigger="change" hx-target="#subsection" hx-swap="outerHTML"
            hx-include="[name='chapter']">
        {options}
    </select>
    '''
    return Markup(select_html)

@app.route('/get_subsections', methods=['POST'])
def get_subsections():
    chapter = request.form.get('chapter', '')
    current_lang = session.get('language', get_locale())
    lang_data = get_data_for_language(current_lang)
    
    filtered_subsections = sorted(set(entry['subsection'] for entry in lang_data if entry['chapter'] == chapter and entry['subsection']))
    options = '<option value="">Alle</option>' + ''.join(f'<option value="{s}">{s}</option>' for s in filtered_subsections)
    select_html = f'''
    <select class="form-select" id="subsection" name="subsection">
        {options}
    </select>
    '''
    return Markup(select_html)

@app.route('/references')
def references():
    return render_template('references.html')

@app.route('/evidence_levels')
def evidence_levels():
    return render_template('evidence_levels.html')

@app.route('/abbreviations')
def abbreviations():
    return render_template('abbreviations.html')

if __name__ == '__main__':
    app.run(debug=True) 