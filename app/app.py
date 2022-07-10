import os
from datetime import datetime

from flask import Flask, request, render_template, send_from_directory
from flask import jsonify
from werkzeug.utils import secure_filename

import meme_generator
import models
from db import Store

from os import environ

from repository.meme_repository import MemeRepository

HOST_URL = environ.get('HOST_URL')
DB_URL = environ.get('DB_URL')
DB_PORT = environ.get('DB_PORT')

if not HOST_URL:
    HOST_URL = 'http://127.0.0.1:5000'

if not DB_URL:
    DB_URL = 'localhost'

if not DB_PORT:
    DB_PORT = 3301

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
        original_file_name = meme.original_image_path.split('/' if '/' in meme.original_image_path else '\\')[-1]
        generated_file_name = meme.generated_image_path.split('/' if '/' in meme.generated_image_path else '\\')[-1]
        read_memes.append(models.GetMeme(id=meme.id,
                                         original_image_url=f'{HOST_URL}/media/{original_file_name}',
                                         generated_image_url=f'{HOST_URL}/media/{generated_file_name}',
                                         top_text=meme.top_text,
                                         bottom_text=meme.bottom_text).dict())

    return jsonify(read_memes), 200


@app.route('/api/memes/<int:pk>/', methods=['GET'])
def get_meme(pk):
    meme = meme_repository.get_meme(pk)
    if not meme:
        return 'Not found', 404

    original_file_name = meme.original_image_path.split('/' if '/' in meme.original_image_path else '\\')[-1]
    generated_file_name = meme.generated_image_path.split('/' if '/' in meme.generated_image_path else '\\')[-1]
    read_meme = models.GetMeme(id=meme.id,
                               original_image_url=f'{HOST_URL}/media/{original_file_name}',
                               generated_image_url=f'{HOST_URL}/media/{generated_file_name}',
                               top_text=meme.top_text,
                               bottom_text=meme.bottom_text)
    return jsonify(read_meme.dict())


@app.route('/api/memes/', methods=['POST'])
def create_meme():
    data = request.form
    files = request.files

    top_text = data.get('top_text')
    bottom_text = data.get('bottom_text')

    form_img = files.get('img')

    # если не передали изображение, то берем случайное
    if not form_img:
        meme_img = meme_repository.get_random_meme_img()
        if not meme_img:
            return 'В базе нет подходящих изображений. Заполните поле `img` самостоятельно', 400
        original_image_path = meme_img.original_image_path
    else:
        now = datetime.now()
        original_file_name = secure_filename(f'{now.strftime("%Y%m%d%M%S")}_{form_img.filename}')
        original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], original_file_name)
        form_img.save(original_image_path)

    # если не передали текст, то берем рандомный
    if not top_text or not bottom_text:
        meme_text = meme_repository.get_random_meme_text()
        if not meme_text:
            return 'В базе нет подходящих изображений. ' \
                   'Заполните поля `top_text` и bottom_text` самостоятельно', 400

        top_text = meme_text.top_text
        bottom_text = meme_text.bottom_text

    generated_image_path = meme_generator.generate_meme(original_image_path, top_text=top_text,
                                                        bottom_text=bottom_text)

    meme = models.Meme(original_image_path=original_image_path,
                       generated_image_path=generated_image_path,
                       top_text=top_text,
                       bottom_text=bottom_text)

    meme = meme_repository.create_meme(meme)

    original_file_name = meme.original_image_path.split('/' if '/' in meme.original_image_path else '\\')[-1]
    generated_file_name = generated_image_path.split('/' if '/' in generated_image_path else '\\')[-1]
    read_meme = models.GetMeme(id=meme.id,
                               original_image_url=f'{HOST_URL}/media/{original_file_name}',
                               generated_image_url=f'{HOST_URL}/media/{generated_file_name}',
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
