from flask import Flask, render_template, request, jsonify
import json
import os
from markupsafe import Markup

app = Flask(__name__)

# JSON laden
DATA_PATH = os.path.join(os.path.dirname(__file__), 'MRI.json')
with open(DATA_PATH, encoding='utf-8') as f:
    data = json.load(f)

# Kapitel und Subsections extrahieren
chapters = sorted(set(entry['chapter'] for entry in data if entry['chapter']))
subsections = sorted(set(entry['subsection'] for entry in data if entry['subsection']))

# Section-Liste extrahieren
sections = sorted(set(entry.get('Section', '') for entry in data if entry.get('Section', '')))

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    selected_section = request.form.get('section') if request.method == 'POST' else ''
    selected_chapter = request.form.get('chapter') if request.method == 'POST' else ''
    selected_subsection = request.form.get('subsection') if request.method == 'POST' else ''
    search_text = request.form.get('search_text', '').strip() if request.method == 'POST' else ''

    if request.method == 'POST':
        results = [entry for entry in data
                   if (not selected_section or entry.get('Section', '') == selected_section)
                   and (not selected_chapter or entry['chapter'] == selected_chapter)
                   and (not selected_subsection or entry['subsection'] == selected_subsection)
                   and (not search_text or search_text.lower() in entry['clinical_situation'].lower())]

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
    filtered_chapters = sorted(set(entry['chapter'] for entry in data if entry.get('Section', '') == section and entry['chapter']))
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