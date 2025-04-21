# PDF Combiner App

A simple web app to upload, combine, and download PDFs using Flask + PyPDF2.

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

Folder Structure
backend/ - Flask backend and upload logic, also static CSS/JS interface

frontend/ - HTML