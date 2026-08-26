import random
from datetime import datetime

from flask import url_for

from . import db
from .constant import (
    AUTO_SHORT_LENGTH,
    GENERATION_FAILED_MESSAGE,
    MAX_GENERATION_ATTEMPTS,
    MAX_LINK_LENGTH,
    MAX_SHORT_LENGTH,
    REDIRECT_VIEW,
    RESERVED_SHORTS,
    SHORT_CHARACTERS,
    SHORT_EXISTS_MESSAGE,
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

    def to_dict(self):
        """Возвращает данные ссылки для ответа API."""
        return {
            'url': self.original,
            'short_link': self.get_short_link(),
        }

    @staticmethod
    def get_by_short(short):
        """Возвращает запись по короткому идентификатору."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def short_exists(short):
        """Проверяет, занято ли короткое имя."""
        return (
            short in RESERVED_SHORTS
            or URLMap.get_by_short(short) is not None
        )

    @staticmethod
    def get_unique_short():
        """Генерирует уникальный короткий идентификатор."""
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short = ''.join(
                random.choices(SHORT_CHARACTERS, k=AUTO_SHORT_LENGTH)
            )
            if not URLMap.short_exists(short):
                return short
        raise RuntimeError(GENERATION_FAILED_MESSAGE)

    @staticmethod
    def create(original, short=None, commit=True):
        """Сохраняет новую запись."""
        if short:
            if URLMap.short_exists(short):
                raise ValueError(SHORT_EXISTS_MESSAGE)
        else:
            short = URLMap.get_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map
