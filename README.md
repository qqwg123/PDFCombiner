# PDF Combiner App

A simple web app to upload, combine, and download PDFs using Flask + PyPDF2.

## 📂 Project Structure

```
pdf_combiner/
├── app/
│   ├── __init__.py       # App initialization
│   ├── routes.py         # Route handlers
│   ├── services/         # Business logic
│   │   ├── __init__.py
│   │   └── pdf_service.py
│   ├── static/           # Static assets
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   ├── templates/        # HTML templates
│   │   └── index.html
│   └── utils/            # Helper functions
│       ├── __init__.py
│       └── file_utils.py
├── config.py             # Configuration
├── uploads/              # Uploaded files (git ignored)
├── run.py                # Application entry point
├── requirements.txt      # Dependencies
├── .gitignore
└── clean.py              # Cleanup script
```

## 🔧 Setup

1. Clone the repo:
```bash
git clone https://github.com/yourusername/pdf-combiner.git
cd pdf-combiner
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python run.py
```

The app will open at http://127.0.0.1:5000

## 📦 Creating an executable

To create a standalone executable:

```bash
pip install pyinstaller

# Windows
pyinstaller --onefile --add-data "app/templates;app/templates" --add-data "app/static;app/static" run.py