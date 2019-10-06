import os
from flask import Flask, request, url_for, render_template, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Skipped - upload folder
ALLOWED_EXTENTIONS = set(['py', 'c', 'cpp', 'js'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        if 'file' not in request.files:
            flash('No file part in form')
        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Do something with file
            return filename
            


if __name__ == '__main__':
    app.run()