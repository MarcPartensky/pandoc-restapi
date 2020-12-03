from flask import Flask
from flask import request, send_file
import pypandoc
import os

app = Flask(__name__)

@app.route('/echo/<text>')
def echo(text:str):
    return text

@app.route('/file/<filename>', methods=['GET', 'POST'])
def file(filename:str):
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'files/{filename}')
        return 'done'
    elif request.method == 'GET':
        ext = filename.split('.')[-1]
        return send_file(f'files/{filename}', mimetype=f'plain/{ext}')

@app.route('/pandoc/<output>', methods=['POST'])
def pandoc(output:str):
    f = request.files['file']
    f.save(f'files/{f.filename}')
    response = pypandoc.convert_file(f'files/{f.filename}', output)
    os.remove(f'files/{f.filename}')
    return response
