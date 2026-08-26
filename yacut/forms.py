from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constant import (
    INVALID_SHORT_MESSAGE,
    LINK_TOO_LONG_MESSAGE,
    MAX_LINK_LENGTH,
    MAX_SHORT_LENGTH,
    SHORT_MATCH_PATTERN,
)

LINK_LABEL = 'Длинная ссылка'
LINK_REQUIRED_MESSAGE = 'Обязательное поле'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
SHORT_TOO_LONG_MESSAGE = (
    f'Слишком длинный вариант короткой ссылки '
    f'(максимальная длина — {MAX_SHORT_LENGTH})'
)
SUBMIT_CREATE_LABEL = 'Создать'
FILES_LABEL = 'Выберите файлы для загрузки'
FILES_REQUIRED_MESSAGE = 'Выберите хотя бы один файл'
SUBMIT_UPLOAD_LABEL = 'Загрузить'


class URLForm(FlaskForm):
    """Форма для ссылок."""

    original_link = URLField(
        LINK_LABEL,
        validators=[
            DataRequired(message=LINK_REQUIRED_MESSAGE),
            URL(),
            Length(max=MAX_LINK_LENGTH, message=LINK_TOO_LONG_MESSAGE),
        ],
    )
    custom_id = StringField(
        SHORT_LABEL,
        validators=[
            Optional(),
            Length(max=MAX_SHORT_LENGTH, message=SHORT_TOO_LONG_MESSAGE),
            Regexp(SHORT_MATCH_PATTERN, message=INVALID_SHORT_MESSAGE),
        ],
    )
    submit = SubmitField(SUBMIT_CREATE_LABEL)


class FileForm(FlaskForm):
    """Форма для страницы c файлами."""

    files = MultipleFileField(
        FILES_LABEL,
        validators=[DataRequired(message=FILES_REQUIRED_MESSAGE)],
    )
    submit = SubmitField(SUBMIT_UPLOAD_LABEL)
