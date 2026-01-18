import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from splitter import split_video, get_video_duration

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['video']
        duration_option = request.form.get('duration')
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Determine split duration
            clip_duration = 30 # default
            if duration_option == '30s':
                clip_duration = 30
            elif duration_option == '1m':
                clip_duration = 60
            elif duration_option == '2m':
                clip_duration = 120
            else:
                 # Check if custom duration was passed? For now stick to options
                 pass

            try:
                # Create a subfolder for this specific upload to avoid collisions
                # For simplicity, we'll just use the filename base
                file_base = os.path.splitext(filename)[0]
                output_dir = os.path.join(app.config['PROCESSED_FOLDER'], file_base)
                
                generated_files = split_video(filepath, clip_duration, output_dir)
                
                return render_template('result.html', files=generated_files, folder=file_base)
            except Exception as e:
                flash(f"Error processing video: {str(e)}")
                return redirect(request.url)
        else:
            flash('Invalid file type')
            return redirect(request.url)

    return render_template('upload.html')

@app.route('/download/<folder>/<filename>')
def download_file(folder, filename):
    directory = os.path.join(app.config['PROCESSED_FOLDER'], folder)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/how-it-works')
def how_it_works():
    # Can be a separate page or section on home.
    # User request asked for "How it works section", likely on home, but can be separate.
    # We'll link to anchor on home or separate page. Let's make it a section on Home for simplicity as per request
    # but if they click nav, maybe redirect to index#how-it-works
    return redirect(url_for('index') + '#how-it-works')

if __name__ == '__main__':
    app.run(debug=True)
