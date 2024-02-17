import os
from host import host
from flask import Flask, request, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("main.html")


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/")

    return render_template("send.html")


@app.route('/receive', methods=['GET', 'POST'])
def receive():
    files = os.listdir(app.config['DOWNLOAD_FOLDER'])
    return render_template("receive.html", files=files)


@app.route('/receive/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = os.path.abspath("data")
    app.config['DOWNLOAD_FOLDER'] = os.path.abspath("data")
    app.run(host=host, port=8000)
