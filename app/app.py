import base64
import json
import os
from datetime import datetime
from io import BytesIO

from flask import Flask, request, redirect, render_template, send_from_directory
from flask import jsonify
from flask_pydantic import validate
from werkzeug.utils import secure_filename

import meme_generator
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
    memes = meme_repository.get_all_memes()

    read_memes = []
    for meme in memes:
        original_file_name = meme.original_image_path.split("\\")[-1]
        generated_file_name = meme.generated_image_path.split("\\")[-1]
        read_memes.append(models.GetMeme(id=meme.id,
                                         original_image_url=f'{HOST_URL}media/{original_file_name}',
                                         generated_image_url=f'{HOST_URL}media/{generated_file_name}',
                                         top_text=meme.top_text,
                                         bottom_text=meme.bottom_text).dict())

    return jsonify(read_memes), 200


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

    now = datetime.now()
    filename = secure_filename(f'{now.strftime("%Y%m%d%M%S")}_{form_img.filename}')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    form_img.save(file_path)

    top_text = data['top_text']
    bottom_text = data['bottom_text']

    generated_image_path = meme_generator.generate_meme(file_path, top_text=top_text, bottom_text=bottom_text)
    generated_file_name = generated_image_path.split('\\')[-1]
    meme = models.Meme(original_image_path=file_path,
                       generated_image_path=generated_image_path,
                       top_text=top_text,
                       bottom_text=bottom_text)

    meme = meme_repository.create_meme(meme)
    read_meme = models.GetMeme(id=meme.id,
                               original_image_url=f'{HOST_URL}media/{filename}',
                               generated_image_url=f'{HOST_URL}media/{generated_file_name}',
                               top_text=top_text,
                               bottom_text=bottom_text)

    return jsonify(read_meme.dict()), 201


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )


if __name__ == '__main__':
    app.run()
