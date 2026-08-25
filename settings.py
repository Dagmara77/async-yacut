import os


class Config(object):
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='SUP3R-S3CR3T-K3Y-F0R-YACUT-PR0J3CT'
    )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    YANDEX_API_URL = 'https://cloud-api.yandex.net/v1/'
    DISK_TOKEN = os.getenv('DISK_TOKEN')
