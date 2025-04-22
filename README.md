# PDF Combiner App

A simple web app to upload, combine, and download PDFs using Flask + PyPDF2.

Folder Structure
backend/ - Flask backend and upload logic, also static CSS/JS interface

frontend/ - HTML

## 🔧 Setup

1. Clone the repo:
```bash
git clone https://github.com/qqwg123/PDFCombiner.git
cd PDFCombiner
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
python backend/app.py
```

The app will open at http://127.0.0.1:5000


5. Create an executable:
```bash
pip install pyinstaller
# Windows
pyinstaller --onefile --add-data "frontend/index.html;frontend" --add-data "backend/static;backend/static" backend/app.py
#macOS/Linux
pyinstaller --onefile --add-data "frontend/index.html:frontend" --add-data "backend/static:backend/static" backend/app.py
```

The executable will be in dist/

## 🧹 Cleaning Up

To clean temporary files and build artifacts:

```bash
python clean.py
```

This will clean:
- PDF files in backend/uploads/
- build/ directory
- dist/ directory
- app.spec file

Add `-v` flag for verbose output:
```bash
python clean.py -v
```