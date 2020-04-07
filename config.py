import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True
    CSRF_ENABLED = True
class Configdb(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'curd.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False