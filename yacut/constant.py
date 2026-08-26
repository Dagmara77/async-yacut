import string

SHORT_CHARACTERS = string.ascii_letters + string.digits
SHORT_MATCH_PATTERN = f'^[{SHORT_CHARACTERS}]+$'
MAX_SHORT_LENGTH = 16
MAX_LINK_LENGTH = 2048
AUTO_SHORT_LENGTH = 6
MAX_GENERATION_ATTEMPTS = 10
FILES_PREFIX = 'files'
RESERVED_SHORTS = (FILES_PREFIX, 'openapi')
REDIRECT_VIEW = 'redirect_view'
GENERATION_FAILED_MESSAGE = (
    f'Не удалось сгенерировать короткий идентификатор '
    f'(лимит попыток — {MAX_GENERATION_ATTEMPTS})'
)
LINK_TOO_LONG_MESSAGE = (
    f'Ссылка слишком длинная (максимальная длина — {MAX_LINK_LENGTH})'
)
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
EMPTY_REQUEST_MESSAGE = 'Отсутствует тело запроса'
URL_REQUIRED_MESSAGE = '"url" является обязательным полем!'
SHORT_NOT_FOUND_MESSAGE = 'Указанный id не найден'
