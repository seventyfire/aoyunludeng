import os
from flask import Flask
from flask import render_template
from program import Program
from material import Material
from flask import request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import base64

UPLOAD_FOLDER = './material'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'wmv', 'avi'}
text_files = {'txt', 'pdf'}
image_files = {'png', 'jpg', 'jpeg', 'gif'}
video_files = {'mp4', 'mov', 'wmv', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'secert key'
CORS(app)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/send_program', methods=['GET', 'POST'])
def send_program():
    json_data = request.args.get('json_data')
    print("======>>>json_data" + json_data)
    program = Program(json_data)
    prog_name = program.send_program()
    print("send program:" + prog_name)
    return {"code": "200", "program_name": prog_name}


@cross_origin()
@app.route('/play_program', methods=['GET', 'POST'])
def play_program():
    program_name = request.args.get('program_name')
    program = Program()
    program.play_program(program_name)
    return {"code": "200"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_type_folder(filename):
    pattern = '.' in filename and filename.rsplit('.', 1)[1].lower()
    if pattern in text_files:
        return 0, "text_files"
    elif pattern in image_files:
        return 1, "image_files"
    elif pattern in video_files:
        return 2, "video_files"


@app.route('/single_upload', methods=['GET', 'POST'])
def upload_file():
    print("upload.......")
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print("\n\n" + str(file.filename) + "\n\n")
        if file and allowed_file(file.filename):
            import time
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            type, folder = get_type_folder(file.filename)
            filename = str(time.time()).replace(".", "")
            material = Material(file, filename, app.config['UPLOAD_FOLDER'] + "/" + folder)
            material.save()
            print("\n\n2" + str(file.filename) + "->" + filename + "\n\n")
            return redirect(url_for('upload_file', filename=filename))

    return {"error": "405"}


@app.route('/multiple_upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'file[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist("file[]")
        # if user does not select file, browser also submit an empty part without filename
        import time
        for file in files:
            print(file.filename)
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                type, folder = get_type_folder(file.filename)
                # filename = secure_filename(file.filename)
                filename = str(time.time()).replace(".", "")
                material = Material(file, filename, app.config['UPLOAD_FOLDER'] + "/" + folder)
                material.save()
                print("\n\n2" + str(file.filename) + "->" + filename + "\n\n")
        return redirect(url_for('upload_file', filename=filename))

    return {"error": "405"}


@app.route('/get_materials', methods=['GET', 'POST'])
def query_material():
    program_name = request.args.get('type')
    if type == 0:  # text
        pass
    elif type == 1:  # image
        pass
    elif type == 2:  # video
        pass
    else:
        return {"error": "404", "message": "type is not found"}


@app.route('/get_test_file', methods=['GET', 'POST'])
def get_test_file():
    path = './material/text_files/test_file.pdf'
    f = open(path, 'rb')
    base64_str = base64.b64encode(f.read())
    return base64_str

# @app.route('/clear')
# def clear_resources():
#     program = Program()
#     program.clear_resources()
#     return "200"


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
