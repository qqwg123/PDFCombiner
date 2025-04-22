from flask import Blueprint, request, send_file, render_template, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from app.services.pdf_service import combine_pdfs
from app.utils.file_utils import allowed_file

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/upload', methods=['POST'])
def upload():
    if 'pdfs' not in request.files:
        return 'No file part', 400

    files = request.files.getlist('pdfs')
    if not files or all(f.filename == '' for f in files):
        return 'No selected file(s)', 400

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    return 'Files uploaded successfully'

@main_bp.route('/remove-file', methods=['POST'])
def remove_file():
    # This endpoint is optional - if a file doesn't exist, we'll just continue
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if filename:
            safe_filename = secure_filename(filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
    except Exception:
        pass
        
    return jsonify({'message': 'Processed'})

@main_bp.route('/combine-and-download', methods=['POST'])
def combine_and_download():
    data = request.get_json()
    filenames = data.get('filenames', [])

    if not filenames:
        return jsonify({'error': 'No filenames provided'}), 400

    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    
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

    # Combine PDFs
    try:
        combine_pdfs(valid_files, output_path)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error combining PDFs: {str(e)}'}), 500

@main_bp.route('/clear-files', methods=['POST'])
def clear_files():
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path) and filename.endswith('.pdf'):
            os.remove(file_path)
    return 'Files cleared', 200