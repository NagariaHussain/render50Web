from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, guess_lexer
from pygments.lexers.special import TextLexer
from weasyprint import CSS, HTML

import os
from flask import Flask, request, url_for, render_template, flash, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Skipped - upload folder
ALLOWED_EXTENTIONS = set(['py', 'c', 'cpp', 'js'])

# get function
# def get(file):
#     try:
#         with open(file, "rb") as f:
#             return f.read().decode("utf-8", "ignore")
#     except Exception as e:
#         if type(e) is FileNotFoundError:
#             raise RuntimeError("Could not find file")



# Rendering
def render(file, size, browser=False, color=True, fontSize="10pt", margin="0.5in", relative=True, title=None):
    """Render file with filename as HTML page(s) of specified size."""
    code = file.read().decode("utf-8", "ignore")

    if code.strip() and color:
        try:
            lexer = get_lexer_for_filename(file.filename)
        except:
                try:
                    assert code.startswith("#!")  # else, e.g., a .gitignore file with a dotfile is mistaken by GuessLexer
                    lexer = guess_lexer(code.splitlines()[0])
                except:
                    lexer = TextLexer()
        string = highlight(code, lexer, HtmlFormatter(linenos="inline", nobackground=True))
    else:
        string = highlight(code, TextLexer(), HtmlFormatter(linenos="inline", nobackground=True))

    if not title:
        title = file.filename
    
    stylesheets = [
            CSS(string="@page {{ border-top: 1px #808080 solid; margin: {}; padding-top: 1em; size: {}; }}".format(margin, size)),
            CSS(string="@page {{ @top-right {{ color: #808080; content: '{}'; padding-bottom: 1em; vertical-align: bottom; }} }}".format(
                title.replace("'", "\'"))),
            CSS(string="* {{ font-family: monospace; font-size: {}; margin: 0; overflow-wrap: break-word; white-space: pre-wrap; }}".format(fontSize)),
            CSS(string=HtmlFormatter().get_style_defs('.highlight')),
            CSS(string=".highlight { background: initial; }"),
            CSS(string=".lineno { color: #808080; }"),
            CSS(string=".lineno:after { content: '  '; }")]
    
    
    HTML(string=string).write_pdf('./tmp/output.pdf', stylesheets=stylesheets)
    

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
            # Do something with file
            render(file, 'A4 landscape')
            return send_file(filename_or_fp='./tmp/output.pdf')
            


if __name__ == '__main__':
    app.run()