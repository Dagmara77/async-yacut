import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constant import (
    EMPTY_REQUEST_MESSAGE,
    INVALID_SHORT_MESSAGE,
    LINK_TOO_LONG_MESSAGE,
    MAX_LINK_LENGTH,
    MAX_SHORT_LENGTH,
    SHORT_NOT_FOUND_MESSAGE,
    SHORT_MATCH_PATTERN,
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
    if len(data['url']) > MAX_LINK_LENGTH:
        raise InvalidAPIUsage(LINK_TOO_LONG_MESSAGE)
    custom_id = data.get('custom_id')
    if custom_id and (
        len(custom_id) > MAX_SHORT_LENGTH
        or not re.match(SHORT_MATCH_PATTERN, custom_id)
    ):
        raise InvalidAPIUsage(INVALID_SHORT_MESSAGE)
    try:
        url_map = URLMap.create(data['url'], custom_id)
    except (ValueError, RuntimeError) as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    """Возвращает оригинальную ссылку по короткому идентификатору."""
    if (url_map := URLMap.get_by_short(short)) is None:
        raise InvalidAPIUsage(SHORT_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.to_dict()['url']})
