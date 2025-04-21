from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger
import os
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

# Clear uploads folder on app start
shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

uploaded_files = []  # Track uploaded file paths

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdfs' not in request.files:
        return jsonify({'success': False, 'message': 'No files part in request'}), 400

    files = request.files.getlist('pdfs')
    if not files or all(f.filename == '' for f in files):
        return jsonify({'success': False, 'message': 'No files selected'}), 400

    uploaded_files.clear()
    for file in files:
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            uploaded_files.append(path)

    return jsonify({'success': True, 'message': f'{len(uploaded_files)} files uploaded'})

@app.route('/combine', methods=['POST'])
def combine():
    if not uploaded_files:
        return jsonify({'success': False, 'message': 'No files uploaded yet'}), 400

    merger = PdfMerger()
    try:
        for path in uploaded_files:
            merger.append(path)
        output_path = os.path.join(UPLOAD_FOLDER, 'combined.pdf')
        merger.write(output_path)
        merger.close()
        return jsonify({'success': True, 'message': 'PDFs combined'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download', methods=['GET'])
def download():
    combined_path = os.path.join(UPLOAD_FOLDER, 'combined.pdf')
    if not os.path.exists(combined_path):
        return jsonify({'success': False, 'message': 'Combined PDF not found'}), 404
    return send_file(combined_path, as_attachment=True)

if __name__ == '__main__':
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run()