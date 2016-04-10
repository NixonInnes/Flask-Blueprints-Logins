import os
import logging
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'somerandomkey')
    APP_NAME = os.getenv('APP_NAME', 'NixFlask')
    APP_ADMIN = os.getenv('APP_ADMIN')
    APP_MAIL_SENDER = os.getenv('APP_MAIL_SENDER', 'localhost')

    LOG_DIR = os.path.join(basedir, 'logs')

    @classmethod
    def make_log_folders(cls):
        if not os.path.exists(cls.LOG_DIR):
            os.makedirs(cls.LOG_DIR)


    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'dev-db.sqlite'))
    LOG_DIR = os.path.join(Config.LOG_DIR, 'dev')

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        cls.make_log_folders()
        log_handler = RotatingFileHandler(
            os.path.join(cls.LOG_DIR, cls.APP_NAME+'.log'),
            maxBytes=10000,
            backupCount=3)
        log_handler.setLevel(logging.INFO)
        app.logger.addHandler(log_handler)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'test-db.sqlite'))
    LOG_DIR = os.path.join(Config.LOG_DIR, 'test')

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        cls.make_log_folders()
        log_handler = RotatingFileHandler(
            os.path.join(cls.LOG_DIR, cls.APP_NAME+'.log'),
            maxBytes=10000,
            backupCount=3)
        log_handler.setLevel(logging.WARN)
        app.logger.addHandler(log_handler)


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'db.sqlite'))

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        cls.make_log_folders()
        log_handler = RotatingFileHandler(
            os.path.join(cls.LOG_DIR, cls.APP_NAME+'.log'),
            maxBytes=10000,
            backupCount=3)
        log_handler.setLevel(logging.ERROR)
        app.logger.addHandler(log_handler)


config = {
    'development': DevConfig,
    'testing':     TestConfig,
    'production':  ProdConfig,
    'default':     DevConfig
}
