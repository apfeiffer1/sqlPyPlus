
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Move the following two lines into the instance/config.py and adapt as needed:
SECRET_KEY = 'secretKey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///data-test.sqlite'

