from datetime import datetime
import time
from uuid import uuid4
import re
from urlparse import urlparse, urljoin

from flask import render_template, current_app, session

from sqlalchemy import inspect, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import text

from . import app
from . import db

# =============================================================================

@app.route('/', methods=['GET'])
def index():

    dbUrl = db.engine.url
    print "got dbUrl:", dbUrl
    engine = create_engine(dbUrl)
    insp = reflection.Inspector.from_engine(engine)

    # sqlite does not return a list for this, just extract it from the URL
    if str(dbUrl).startswith('sqlite:'):
        current_app.isSqlite = True
        dbList = [ str(dbUrl).split('/')[-1] ]
    else:
        sysList = [u'information_schema', u'mysql', u'performance_schema', u'sys']
        dbList = [ x for x in insp.get_schema_names() if x not in sysList ]
    print "dbList: ", dbList
    
    return render_template( 'main.html', dbNames=dbList, form=None )

@app.route('/showDB/<string:dbName>')
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
def showFullTable(tableName):

    return showTableContent(tableName, -1)

@app.route( '/showTable/<string:tableName>' )
def showTable( tableName ) :

    return showTableContent(tableName, 100)

def showTableContent( tableName, nRows ):

    print "session:", session
    dbName = session.get('dbName')

    print 'dbName: ', dbName
    dbUrl = str(db.engine.url)
    print 'engine: ', dbUrl

    # engine = create_engine( session.get('engine') )
    insp = reflection.Inspector.from_engine( db.engine )

    meta = MetaData()
    selTable = Table(tableName, meta)

    if str(dbUrl).startswith('sqlite:'):
        colHeaders = [ x['name'] for x in insp.get_columns(table_name=tableName)]
    else:
        colHeaders = [ x['name'] for x in insp.get_columns(table_name=tableName, schema=dbName)]
    insp.reflecttable(selTable, None)

    limitStr = ' '
    if nRows > 0:
        limitStr = ' limit %d' % nRows
    if str(dbUrl).startswith('sqlite:'):
        sel = text( 'select * from %s%s' % (tableName, limitStr) )
    else:
        sel = text( 'select * from %s.%s%s' % (dbName, tableName, limitStr) )
    print '++> ', sel

    data = db.session.execute( sel ).fetchall()

    # print "table=", selTable
    # print 'cols =', colHeaders
    # print 'data:', data

    return render_template( 'showTable.html', 
                            tableName=tableName, dbName=dbName,
                            colHeaders=colHeaders, data=data )

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
