import base64
import os
from io import BytesIO

from flask import Flask, request, redirect, render_template
from flask import jsonify
from flask_pydantic import validate
from werkzeug.utils import secure_filename

import models
from db import Store
import qrcode

from os import environ

from repository.meme_repository import MemeRepository

HOST_URL = environ.get('HOST_URL')
DB_URL = environ.get('DB_URL')
DB_PORT = environ.get('DB_PORT')

if not HOST_URL:
    HOST_URL = 'http://127.0.0.1:5000/'

if not DB_URL:
    DB_URL = 'localhost'

if not DB_PORT:
    DB_PORT = 3301
print('alloooo')
print(HOST_URL, DB_URL, DB_PORT)

UPLOAD_FOLDER = 'media'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = Store(url=DB_URL, port=DB_PORT)

meme_repository = MemeRepository(db)


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/api/memes/', methods=['GET'])
def get_all_memes():
    meme_repository.get_all_memes()
    return 'kkeee', 200


@app.route('/api/memes/', methods=['POST'])
def create_meme():
    data = request.form
    files = request.files

    if not data.get('top_text'):
        return 400, '`top_text` обязательное поле'
    if not data.get('bottom_text'):
        return 400, '`top_text` обязательное поле'
    if not files.get('img') or not files['img'].filename:
        return 400, '`img` обязательное поле'

    form_img = files['img']

    original_image_path = os
    filename = secure_filename(form_img.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    form_img.save(file_path)
    print(file_path)

    meme = models.Meme(**data)
    print(meme)

    meme = meme_repository.create_meme(meme)
    return meme.json(), 201


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
