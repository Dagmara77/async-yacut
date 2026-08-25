from pathlib import Path

import aiohttp
from flask import flash, redirect, render_template, send_file

from yacut import app
from .constant import REDIRECT_VIEW
from .forms import FileForm, URLForm
from .models import URLMap
from .utils import YandexDiskError, upload_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница с формой для ссылок."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data or None,
            validated=True,
        )
    except (ValueError, RuntimeError) as error:
        flash(str(error))
        return render_template('index.html', form=form)
    return render_template(
        'index.html', form=form, short_link=url_map.get_short_link()
    )


@app.route('/openapi')
def openapi_view():
    """Отдаёт спецификацию API из файла openapi.yml."""
    return send_file(
        Path(app.root_path).parent / 'openapi.yml', mimetype='text/yaml'
    )


@app.route('/<string:short>', endpoint=REDIRECT_VIEW)
def redirect_view(short):
    """Редиректит пользователя на оригинальный адрес."""
    return redirect(URLMap.get(short, or_404=True).original)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    """Страница загрузки файлов на Яндекс Диск."""
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = [(file.filename, file.read()) for file in form.files.data]
    try:
        links = upload_files(files)
    except (aiohttp.ClientError, KeyError, YandexDiskError) as error:
        flash(str(error))
        return render_template('files.html', form=form)
    try:
        url_maps = [
            URLMap.create(link, commit=(i == len(links) - 1))
            for i, link in enumerate(links)
        ]
    except (ValueError, RuntimeError) as error:
        flash(str(error))
        return render_template('files.html', form=form)
    return render_template(
        'files.html',
        form=form,
        uploaded_files=[
            {'filename': filename, 'short_link': url_map.get_short_link()}
            for (filename, _), url_map in zip(files, url_maps)
        ],
    )
