import os
from decouple import config
from datetime import timedelta

class config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')

class DevConfig(config):
    DEBUG=config()
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:OPEyemi2001@localhost/lms'
    SQLALCHEMY_TRACK_MODIFICATIONS=False


class TestConfig(config):
    TESTING=True
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:OPEyemi2001@localhost/lms'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class ProdConfig(config):
    pass

config_dict = {
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}