from datetime import datetime
import time
from uuid import uuid4
import re
from urlparse import urlparse, urljoin
from functools import wraps

from flask import render_template, current_app, session, redirect, url_for

from sqlalchemy import inspect, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import text
from sqlalchemy.orm import exc as sa_exc

from . import app
from . import db


def check_crashed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print "==> crash detected, redirecting to index"
            return redirect( url_for('index') )

    return decorated_function
# =============================================================================

@app.route('/', methods=['GET'])
def index():

    dbUrl = db.engine.url
    # print "db at: ", dbUrl

    engine = create_engine(dbUrl)
    insp = reflection.Inspector.from_engine(engine)

    # sqlite does not return a list for this, just extract it from the URL
    if str(dbUrl).startswith('sqlite:'):
        current_app.isSqlite = True
        dbList = [ str(dbUrl).split('/')[-1] ]
    else:
        sysList = [u'information_schema', u'mysql', u'performance_schema', u'sys']
        dbList = [ x for x in insp.get_schema_names() if x not in sysList ]
    # print "dbList: ", dbList
    
    return render_template( 'main.html', dbNames=dbList, form=None )

@app.route('/showDB/<string:dbName>')
@check_crashed
def showDB(dbName):

    session['dbName'] = dbName
    current_app.dbName = dbName
    
    dbUrl = str(db.engine.url)
    engine = create_engine( dbUrl )
    current_app.theEngine = engine
    
    insp = reflection.Inspector.from_engine( current_app.theEngine )

    ignoreList = [] # ['alembic_version']
    if str(dbUrl).startswith('sqlite:'):
        tableNames = [ x for x in insp.get_table_names() if x not in ignoreList]
    else:
        tableNames = [ x for x in insp.get_table_names(schema=dbName) if x not in ignoreList]

    return render_template( 'showDB.html', tableNames = tableNames, dbName=dbName )

@app.route('/showFullTable/<string:tableName>')
@check_crashed
def showFullTable(tableName):

    return showTableContent(tableName, -1)

@app.route( '/showTable/<string:tableName>' )
@check_crashed
def showTable( tableName ) :

    return showTableContent(tableName, 100)


def showTableContent( tableName, nRows ):

    info = {}
    errors = {}

    info["session"] = session
    dbName = session.get('dbName')
    info['dbName'] = dbName

    dbUrl = str(db.engine.url)
    info['engine'] = dbUrl

    meta = MetaData()
    selTable = Table('%s.%s' % (dbName,tableName), meta)

    # engine = create_engine( session.get('engine') )
    insp = reflection.Inspector.from_engine( db.engine )

    # try:
    #     insp.reflecttable(selTable, None)
    # except Exception as e:
    #     errors['NoSuchTableError'] = 'reflecttable> Table %s.%s not found or not accessible.' % (dbName, tableName, )

    if str(dbUrl).startswith('sqlite:'):
        colHeaders = [ x['name'] for x in insp.get_columns(table_name=tableName)]
    else:
        colHeaders = [ x['name'] for x in insp.get_columns(table_name=tableName, schema=dbName)]

    limitStr = ' '
    if nRows > 0:
        limitStr = ' limit %d' % nRows
    if str(dbUrl).startswith('sqlite:'):
        sel = text( 'select * from %s%s' % (tableName, limitStr) )
    else:
        sel = text( 'select * from %s.%s%s' % (dbName, tableName, limitStr) )

    data = db.session.execute( sel ).fetchall()

    return render_template( 'showTable.html',
                            tableName=tableName,
                            dbName=dbName,
                            colHeaders=colHeaders,
                            data=data,
                            info=info, errors=errors )

@app.route('/showTableSchema/<string:tableName>')
def showTableSchema(tableName):

    dbName = session.get('dbName')

    dbUrl = str(db.engine.url)
    insp = reflection.Inspector.from_engine( db.engine )

    meta = MetaData()
    selTable = Table(tableName, meta)

    print "insp: ", insp.default_schema_name, insp.bind, insp.dialect, insp.engine

    if str(dbUrl).startswith('sqlite:'):
        colInfo = insp.get_columns(table_name=tableName)
    else:
        colInfo = insp.get_columns(table_name=tableName, schema=dbName)
    # print insp.reflecttable(selTable, None)

    return render_template( 'showTableSchema.html',
                            tableName=tableName, dbName=dbName,
                            colInfo=colInfo )
