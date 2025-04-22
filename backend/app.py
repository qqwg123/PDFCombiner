from flask import Flask, request, send_file, render_template_string, jsonify
import os
import sys
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

app = Flask(__name__,
            static_folder=get_resource_path('backend/static'),
            template_folder=get_resource_path('frontend'))

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_file(get_resource_path(os.path.join('backend', 'static', filename)))

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Clear existing files on startup
for filename in os.listdir(UPLOAD_FOLDER):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(file_path) and filename.endswith('.pdf'):
        os.remove(file_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    html_path = get_resource_path(os.path.join('frontend', 'index.html'))
    with open(html_path, 'r', encoding='utf-8') as f:
        return render_template_string(f.read())

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdfs' not in request.files:
        return 'No file part', 400

    files = request.files.getlist('pdfs')
    if not files or all(f.filename == '' for f in files):
        return 'No selected file(s)', 400

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return 'Files uploaded successfully'

@app.route('/remove-file', methods=['POST'])
def remove_file():
    # This endpoint is optional - if a file doesn't exist, we'll just continue
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if filename:
            safe_filename = secure_filename(filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
    except Exception:
        pass
        
    return jsonify({'message': 'Processed'})

@app.route('/combine-and-download', methods=['POST'])
def combine_and_download():
    data = request.get_json()
    filenames = data.get('filenames', [])

    if not filenames:
        return jsonify({'error': 'No filenames provided'}), 400

    # Ensure all files exist and are valid PDFs (security)
    valid_files = []
    for fname in filenames:
        path = os.path.join(UPLOAD_FOLDER, secure_filename(fname))
        if os.path.exists(path) and path.endswith('.pdf') and fname != 'combined.pdf':
            valid_files.append(path)

    if not valid_files:
        return jsonify({'error': 'No valid PDF files to combine'}), 400

    output_path = os.path.join(UPLOAD_FOLDER, 'combined.pdf')
    if os.path.exists(output_path):
        os.remove(output_path)

    merger = PdfMerger()
    for path in valid_files:
        merger.append(path)
    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)


@app.route('/clear-files', methods=['POST'])
def clear_files():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path) and filename.endswith('.pdf'):
            os.remove(file_path)
    return 'Files cleared', 200


if __name__ == '__main__':
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run()