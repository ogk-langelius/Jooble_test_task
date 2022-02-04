import os
from typing import List, Type


class BaseConfig:
    CONFIG_NAME = 'base'
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = 'dev'
    SECRET_KEY = os.getenv('DEV_SECRET_KEY')
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@db:5432/app_dev'.format(
        os.getenv('POSTGRES_USER'),
        os.getenv('POSTGRES_PASSWORD'))


class TestingConfig(BaseConfig):
    CONFIG_NAME = 'test'
    SECRET_KEY = os.getenv('TEST_SECRET_KEY')
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PASS = os.getenv('POSTGRES_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@db:5432/app_dev'.format(
        os.getenv('POSTGRES_USER'),
        os.getenv('POSTGRES_PASSWORD'))


class ProdConfig(BaseConfig):
    CONFIG_NAME = 'prod'
    SECRET_KEY = os.getenv('PROD_SECRET_KEY')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PASS = os.getenv('POSTGRES_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@localhost:5432/app-prod'.format(
        os.getenv('POSTGRES_USER'),
        os.getenv('POSTGRES_PASSWORD'))


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
