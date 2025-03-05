import os
import subprocess
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pptx'}
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024  # 1GB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a PPTX file.')
        return redirect(url_for('index'))

    try:
        # Ensure upload directory exists
        ensure_dir(app.config['UPLOAD_FOLDER'])
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        pptx_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pptx_path)
        
        # Convert to PDF using LibreOffice
        pdf_filename = os.path.splitext(filename)[0] + '.pdf'
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        
        # Execute LibreOffice conversion
        process = subprocess.run([
            'libreoffice',
            '--headless',
            '--convert-to',
            'pdf',
            '--outdir',
            app.config['UPLOAD_FOLDER'],
            pptx_path
        ], capture_output=True, text=True)
        
        if process.returncode != 0:
            raise Exception(f"Conversion failed: {process.stderr}")
        
        # Send the converted PDF file
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=pdf_filename
        )
    
    except Exception as e:
        flash(f'An error occurred during conversion: {str(e)}')
        return redirect(url_for('index'))
    
    finally:
        # Clean up temporary files
        try:
            if os.path.exists(pptx_path):
                os.remove(pptx_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception as e:
            print(f"Error cleaning up files: {e}")

if __name__ == '__main__':
    app.run(debug=True)
