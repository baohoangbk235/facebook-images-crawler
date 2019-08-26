from flask import Flask, send_from_directory, request
import json
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/baohoang235/Downloads/facebook-images-crawler/server"

@app.route('/', methods=['POST'])
def handle_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    class_dir_name = request.form.get("class")
    print(class_dir_name)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'],class_dir_name)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    file.save(os.path.join(save_path, filename))
    return 'success'

if __name__ == '__main__':
    app.run(debug=True)