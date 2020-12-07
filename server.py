from flask import Flask
from flask import request, send_file, render_template, send_from_directory
import os
import glob
import shlex
import shutil
import urllib

app = Flask(__name__)
root_path = os.getcwd()
files_path = os.getcwd() + '/files'
zip_path = os.getcwd() + '/zip'

def clean():
    """Clean the files folder."""
    files = glob.glob('files/*')
    for f in files:
        os.remove(f)
    files = glob.glob('zip/*')
    for f in files:
        os.remove(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/echo/<text>')
def echo(text:str):
    return text

@app.route('/file/<filename>', methods=['GET', 'POST'])
def file(filename:str):
    filename = urllib.parse.unquote(filename)
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'files/{filename}')
        return 'done'
    elif request.method == 'GET':
        # ext = filename.split('.')[-1]
        return send_file(f'files/{filename}')
# , mimetype=f'plain/{ext}'

def convert(output, request):
    """Convert the request files into output using pandoc."""
    os.chdir(files_path)
    output_args = shlex.split(output)
    filenames = []
    for file in request.files.values():
        file.save(file.filename)
        filenames.append(file.filename)
    if len(output_args) == 0:
        raise Exception('Output field is empty!')
    elif len(output_args) > 1:
        if output_args[0] != 'pandoc':
            output_args = ['pandoc'] + output_args
        cmd = shlex.join(output_args)
        output_file = output_args[-1]
    elif len(output.split('.'))>1:
        output_file = output
        cmd = f"pandoc {filenames[0]} -o {output_file}"
    elif len(filenames)==1:
        format = output
        output_file = ''.join(filenames[-1].split('.')[:-1]) + '.' + format
        cmd = f"pandoc {filenames[0]} -o {output_file}"
    else:
        format = output
        output_file = 'unknown.' + format

    # f = list(request.files.keys())
    # print(os.listdir('files'))
    # os.remove(f'files/{f.filename}')
    print(cmd)
    os.system(cmd)
    os.chdir(root_path)

    # Zipping
    output_root, output_extension = os.path.splitext(output_file)

    shutil.make_archive(
        zip_path +'/'+output_root+'-project', 'zip', files_path)
    shutil.move(zip_path+'/'+output_root+'-project.zip', files_path)
    return (output_file, filenames)

@app.route('/form', methods=['POST'])
def pandoc_form():
    """GUI view"""
    clean()
    output = request.form['output']

    output_file, filenames = convert(
        output, request
    )
    output_root, output_extension = os.path.splitext(output_file)
    output_zip = output_root+'-project.zip'
    if output_extension == '.html' and len(filenames) > 1:
        return output_zip
    return output_file

@app.route('/api/<output>', methods=['POST'])
def pandoc(output:str):
    """API view"""
    clean()
    output = urllib.parse.unquote(output)

    output_file, filenames = convert(
        output, request
    )
    output_root, output_extension = os.path.splitext(output_file)
    output_zip = output_root+'-project.zip'

    if 'zip' in request.args:
        return send_from_directory(files_path, output_zip)
    else:
        return send_from_directory(files_path, output_file)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
