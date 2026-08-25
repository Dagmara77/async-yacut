import asyncio
import urllib.parse
from http import HTTPStatus

import aiohttp
from flask import current_app

DISK_ERROR_MESSAGE = 'Ошибка при обращении к Яндекс Диску, код ответа: {}'


class YandexDiskError(Exception):
    """Ошибка при загрузке файла на Яндекс Диск."""


async def upload_file_to_yandex_disk(session, file_bytes, filename):
    """Загружает файл на Яндекс Диск и возвращает ссылку для скачивания."""
    api_url = current_app.config['YANDEX_API_URL']
    headers = {
        'Authorization': f"OAuth {current_app.config['DISK_TOKEN']}"
    }
    async with session.get(
        f'{api_url}disk/resources/upload',
        headers=headers,
        params={  # noqa: E231
            'path': 'app:/' + filename,
            'overwrite': 'true'
        },
    ) as response:
        if response.status != HTTPStatus.OK:
            raise YandexDiskError(
                DISK_ERROR_MESSAGE.format(response.status)
            )
        upload_url = (await response.json())['href']

    async with session.put(upload_url, data=file_bytes) as response:
        if response.status != HTTPStatus.CREATED:
            raise YandexDiskError(
                DISK_ERROR_MESSAGE.format(response.status)
            )
        location = response.headers['Location']

    location = urllib.parse.unquote(location).replace('/disk', '', 1)
    async with session.get(
        f'{api_url}disk/resources/download',
        headers=headers,
        params={'path': location},
    ) as response:
        if response.status != HTTPStatus.OK:
            raise YandexDiskError(
                DISK_ERROR_MESSAGE.format(response.status)
            )
        return (await response.json())['href']


def upload_files(files):
    """Загружает набор файлов и возвращает список ссылок для скачивания."""
    async def _run():
        async with aiohttp.ClientSession() as session:
            tasks = [
                upload_file_to_yandex_disk(session, file_bytes, filename)
                for filename, file_bytes in files
            ]
            return await asyncio.gather(*tasks)

    return asyncio.run(_run())
