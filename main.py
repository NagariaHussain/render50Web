from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        return 'TODO'


if __name__ == '__main__':
    app.run()