# National Minimum Retesting Intervals in Pathology

A multilingual web application for searching and filtering medical retesting interval guidelines. The application provides a user-friendly interface to browse pathology guidelines in multiple languages with professional medical organization branding.

## Features

- **Multilingual Support**: Currently supports English and German with easy language switching
- **Professional Branding**: Features logos from IBMS, Royal College of Pathologists, and Association of Clinical Biochemistry
- **Advanced Filtering**: Filter by Section, Chapter, Subsection, and clinical situation
- **Real-time Search**: Instant search with highlighting of matching terms
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dynamic Dropdowns**: HTMX-powered cascading dropdown menus
- **Complete Data**: Includes references, sources, and evidence levels

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: Bootstrap 5, HTMX
- **Internationalization**: Flask-Babel
- **Data Format**: JSON
- **Styling**: Bootstrap CSS framework

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/drfoehn/mri.git
   cd mri
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`

## Data Structure

The application uses `MRI_en_de.json` which contains medical guidelines with the following structure:

```json
{
    "chapter": "2.1 Renal (refers to the measurement of U&E, unless otherwise stated)",
    "clinical_situation": "Normal follow up",
    "entry_id": 1,
    "id": 1,
    "lang": "en",
    "recommendation": "A repeat would be indicated on clinical grounds...",
    "section": "Biochemistry",
    "subsection": null,
    "ref": "B-R1",
    "source": "Consensus opinion of the relevant expert working group",
    "level_of_evidence": "GPP"
}
```

## Adding New Languages

To add support for new languages (e.g., Spanish, French), follow these steps:

### Step 1: Prepare Translation Data

1. **Create a new JSON file** with translated entries:
   ```json
   {
       "chapter": "2.1 Renal (refiere a la medición de U&E, salvo que se indique lo contrario)",
       "clinical_situation": "Seguimiento normal",
       "entry_id": 1,
       "id": 401,
       "lang": "es",
       "recommendation": "Una repetición estaría indicada por motivos clínicos...",
       "section": "Bioquímica",
       "subsection": null,
       "ref": "B-R1",
       "source": "Opinión consensuada del grupo de trabajo experto relevante",
       "level_of_evidence": "GPP"
   }
   ```

2. **Use the import script** (`import_translation_json.py`) as a reference:
   ```python
   # Modify the JSON_PATH to point to your new language file
   JSON_PATH = 'path/to/spanish_data.json'
   ```

### Step 2: Update Application Configuration

1. **Add the new language to Flask-Babel configuration** in `app.py`:
   ```python
   app.config['LANGUAGES'] = {
       'en': 'English',
       'de': 'German',
       'es': 'Spanish',  # Add new language
       'fr': 'French'    # Add another language
   }
   ```

### Step 3: Create Translation Files

1. **Extract translatable strings**:
   ```bash
   pybabel extract -F babel.cfg -k _l -o messages.pot .
   ```

2. **Create translation files for new languages**:
   ```bash
   # For Spanish
   pybabel init -i messages.pot -d translations -l es
   
   # For French
   pybabel init -i messages.pot -d translations -l fr
   ```

3. **Translate the UI strings** in the generated `.po` files:
   - Edit `translations/es/LC_MESSAGES/messages.po`
   - Edit `translations/fr/LC_MESSAGES/messages.po`
   
   Example:
   ```po
   #: templates/index.html:35
   msgid "National minimum retesting intervals in pathology"
   msgstr "Intervalos mínimos nacionales de retest en patología"
   ```

4. **Compile translations**:
   ```bash
   pybabel compile -d translations -l es
   pybabel compile -d translations -l fr
   ```

### Step 4: Update Template

1. **Add language option** in `templates/index.html`:
   ```html
   <li><a class="dropdown-item" href="{{ url_for('set_language', language='es') }}">Español</a></li>
   <li><a class="dropdown-item" href="{{ url_for('set_language', language='fr') }}">Français</a></li>
   ```

### Step 5: Merge Translation Data

1. **Combine existing data** with new language entries:
   - Merge your new language JSON with `MRI_en_de.json`
   - Ensure `entry_id` matches between languages for the same content
   - Update `id` to be unique for each language entry

2. **Use the merge script** (similar to `fix_german_refs.py`) to ensure consistency:
   ```python
   # Create a script to merge new language data
   # Ensure ref, source, level_of_evidence are consistent across languages
   ```

### Step 6: Test and Deploy

1. **Test the new language**:
   - Start the application
   - Switch to the new language
   - Verify all data displays correctly
   - Test filtering and search functionality

2. **Update documentation**:
   - Update this README with the new language
   - Update any deployment documentation

## File Structure

```
mri/
├── app.py                          # Main Flask application
├── MRI_en_de.json                  # Multilingual data file
├── requirements.txt                # Python dependencies
├── babel.cfg                       # Babel configuration
├── templates/
│   └── index.html                  # Main template
├── translations/                   # Translation files
│   ├── de/LC_MESSAGES/            # German translations
│   ├── es/LC_MESSAGES/            # Spanish translations (to be created)
│   └── fr/LC_MESSAGES/            # French translations (to be created)
├── static/
│   └── images/                    # Logo files
├── images/                        # Original logo files
└── import_translation_json.py     # Reference script for data import
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Authors

- **Dr Tim Lang**, County Durham and Darlington NHS Foundation Trust
- **Dr Bernie Croal**, Aberdeen Royal Infirmary, NHS Grampian

## Application Development

**Application by Janne Cadamuro** with the [LabMed Alliance](https://labmedalliance.com)

## License

This project is developed for medical professionals and follows medical data standards. Please ensure compliance with local medical data regulations when using or modifying this application.

## Support

For technical support or questions about adding new languages, please open an issue in the GitHub repository.
