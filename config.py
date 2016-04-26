
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'aVerySecretAndHardToGuessKey'

SQLALCHEMY_DATABASE_URI = 'sqlite:///data-test.sqlite'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

