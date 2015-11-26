
from app import app, db
from flask import render_template, redirect, url_for

from sqlalchemy.engine import reflection
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import text
from .forms import InputDB

from netrc import netrc

@app.route('/')
@app.route('/index')
def index():

    return show()

@app.route('/show')
def show():

    engine = db.engine
    insp = reflection.Inspector.from_engine(engine)

    ignoreList = [] # ['alembic_version']
    tableNames = [ x for x in insp.get_table_names() if x not in ignoreList]

    # print "got tablesnames:", tableNames

    return render_template( 'overview.html', tableNames = tableNames )


@app.route('/showTable/<string:tableName>')
def showTable(tableName):

    meta = MetaData()
    selTable = Table(tableName, meta)

    insp = reflection.Inspector.from_engine(db.engine)

    colHeaders = [ x['name'] for x in insp.get_columns(table_name=tableName)]
    insp.reflecttable(selTable, None)

    sel = text( 'select * from %s' % tableName )
    data = db.session.execute( sel ).fetchall()

    # print "table=", selTable
    # print 'cols =', colHeaders
    # print 'data:', data

    return render_template( 'showTable.html', tableName=tableName, colHeaders=colHeaders, data=data )
