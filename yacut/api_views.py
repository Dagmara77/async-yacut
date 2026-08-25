from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constant import (
    EMPTY_REQUEST_MESSAGE,
    SHORT_NOT_FOUND_MESSAGE,
    URL_REQUIRED_MESSAGE,
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создаёт короткую ссылку и возвращает её в формате JSON."""
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST_MESSAGE)
    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage(URL_REQUIRED_MESSAGE)
    try:
        url_map = URLMap.create(data['url'], data.get('custom_id'))
    except (ValueError, RuntimeError) as error:
        raise InvalidAPIUsage(str(error))
    return jsonify({
        'url': data['url'],
        'short_link': url_map.get_short_link(),
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    """Возвращает оригинальную ссылку по короткому идентификатору."""
    if (url_map := URLMap.get(short)) is None:
        raise InvalidAPIUsage(SHORT_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
