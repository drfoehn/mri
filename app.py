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
DATA_PATH = os.path.join(os.path.dirname(__file__), 'MRI.json')
with open(DATA_PATH, encoding='utf-8') as f:
    all_data = json.load(f)

def get_filtered_data(language):
    """Filter data by language"""
    if language == 'de':
        return [entry for entry in all_data if entry.get('lang') == 'de']
    else:
        return [entry for entry in all_data if entry.get('lang') == 'en']

def get_data_for_current_language():
    """Get data filtered by current language"""
    current_language = get_locale()
    return get_filtered_data(current_language)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get data filtered by current language
    data = get_data_for_current_language()
    
    # Extract sections, chapters, and subsections from filtered data
    sections = sorted(set(entry.get('section', '') for entry in data if entry.get('section', '')))
    chapters = sorted(set(entry['chapter'] for entry in data if entry['chapter']))
    subsections = sorted(set(entry['subsection'] for entry in data if entry['subsection']))
    
    results = []
    selected_section = request.form.get('section') if request.method == 'POST' else ''
    selected_chapter = request.form.get('chapter') if request.method == 'POST' else ''
    selected_subsection = request.form.get('subsection') if request.method == 'POST' else ''
    search_text = request.form.get('search_text', '').strip() if request.method == 'POST' else ''

    if request.method == 'POST' and (selected_section or selected_chapter or selected_subsection or search_text):
        filtered_results = [entry for entry in data
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

    return render_template('index.html',
                           sections=sections,
                           chapters=chapters,
                           subsections=subsections,
                           results=results,
                           selected_section=selected_section,
                           selected_chapter=selected_chapter,
                           selected_subsection=selected_subsection,
                           search_text=search_text)

@app.route('/get_chapters', methods=['POST'])
def get_chapters():
    section = request.form.get('section', '')
    data = get_data_for_current_language()
    filtered_chapters = sorted(set(entry['chapter'] for entry in data if entry.get('section', '') == section and entry['chapter']))
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
    data = get_data_for_current_language()
    filtered_subsections = sorted(set(entry['subsection'] for entry in data if entry['chapter'] == chapter and entry['subsection']))
    options = '<option value="">Alle</option>' + ''.join(f'<option value="{s}">{s}</option>' for s in filtered_subsections)
    select_html = f'''
    <select class="form-select" id="subsection" name="subsection">
        {options}
    </select>
    '''
    return Markup(select_html)

if __name__ == '__main__':
    app.run(debug=True) 