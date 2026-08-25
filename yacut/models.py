import random
import re
from datetime import datetime

from flask import url_for

from . import db
from .constant import (
    AUTO_SHORT_LENGTH,
    GENERATION_FAILED_MESSAGE,
    INVALID_SHORT_MESSAGE,
    LINK_TOO_LONG_MESSAGE,
    MAX_GENERATION_ATTEMPTS,
    MAX_LINK_LENGTH,
    MAX_SHORT_LENGTH,
    REDIRECT_VIEW,
    RESERVED_SHORTS,
    SHORT_CHARACTERS,
    SHORT_EXISTS_MESSAGE,
    SHORT_MATCH_PATTERN,
)


class URLMap(db.Model):
    """Модель для хранения оригинальных и коротких ссылок."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_short_link(self):
        """Возвращает полную короткую ссылку."""
        return url_for(REDIRECT_VIEW, short=self.short, _external=True)

    @staticmethod
    def get(short, or_404=False):
        """Возвращает запись по короткому идентификатору."""
        query = URLMap.query.filter_by(short=short)
        return query.first_or_404() if or_404 else query.first()

    @staticmethod
    def get_unique_short():
        """Генерирует уникальный короткий идентификатор."""
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short = ''.join(
                random.choices(SHORT_CHARACTERS, k=AUTO_SHORT_LENGTH)
            )
            if short not in RESERVED_SHORTS and not URLMap.get(short):
                return short
        raise RuntimeError(GENERATION_FAILED_MESSAGE)

    @staticmethod
    def create(original, short=None, validated=False, commit=True):
        """Проверяет данные и сохраняет новую запись."""
        if not validated:
            if len(original) > MAX_LINK_LENGTH:
                raise ValueError(LINK_TOO_LONG_MESSAGE)
            if short and (len(short) > MAX_SHORT_LENGTH
                          or not re.match(SHORT_MATCH_PATTERN, short)):
                raise ValueError(INVALID_SHORT_MESSAGE)
        if short:
            if short in RESERVED_SHORTS or URLMap.get(short):
                raise ValueError(SHORT_EXISTS_MESSAGE)
        else:
            short = URLMap.get_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map
