from flask import Flask, request, send_file, render_template_string, jsonify
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger

app = Flask(__name__)
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
    with open(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html'), 'r', encoding='utf-8') as f:
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

@app.route('/combine-and-download', methods=['POST'])
def combine_and_download():
    pdf_files = sorted(
    [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')],
    key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x))
)


    if not pdf_files:
        return jsonify({'error': 'No PDF files uploaded'}), 400

    merger = PdfMerger()
    for filename in pdf_files:
        merger.append(os.path.join(UPLOAD_FOLDER, filename))
    output_path = os.path.join(UPLOAD_FOLDER, 'combined.pdf')
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
