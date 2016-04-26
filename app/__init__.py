
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

logging.basicConfig()
sqlLogger = logging.getLogger("myapp.sqltime")
sqlLogger.setLevel(logging.WARNING)

logger = logging.getLogger("DbExplorer")
logger.setLevel(logging.INFO)

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy( session_options={'autoflush':False, 'autocommit':False} )

app = Flask(__name__)
app.config.from_object('config')

bootstrap.init_app(app)
moment.init_app(app)
db.init_app(app)

from app import views
