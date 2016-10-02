"""
    Connect to a vertica database and run queries
"""
from flask import g
from vertica-python.vertica_python import *

import re
import os

DB_NAME = 'test'
DB_USER = 'dbadmin'
DB_PASSWORD = ''
DB_HOST = os.environ['DB_HOST']

conn_info = {'host': DB_HOST,
             'port': 5433,
             'user': 'dbadmin',
             'password': '',
             'database': 'test',
             # 10 minutes timeout on queries
             'read_timeout': 600,
             # default throw error on invalid UTF-8 results
             'unicode_error': 'strict',
             # SSL is disabled by default
             'ssl': False}

def make_dicts(cursor, row):
    """
        Turn query results into dictionaries keyed by column name
    """
    # print 'in make_dicts()'
    colnames = [col[0] for col in cursor.description]

    fmtrow = {}
    for idx, value in enumerate(row):
      fmtrow[colnames[idx]] = value

    return fmtrow

def get_db():
    # print "in get_db()"
    db = getattr(g, '_database', None)
    # print 'succeeded getattr()'
    if db is None:
        # print 'db is none'
        db = g._database = vertica_python.connect(**conn_info)
    # print 'out of if statement'
    return db


def query_db(query, args=(), one=False):
    # print 'in query_db'
    print query
    cur = get_db().cursor()

    try:
        cur.execute(query, args)
        rv = cur.fetchall()

        # Turn into colname->val dict representation of tuple
        # this isn't very efficient but will suffice for now
        rv = [make_dicts(cur, row) for row in rv]
    except Exception, e:
        print e
        rv = [{'error': e}]

    cur.close()
    return (rv[0] if rv else None) if one else rv

def select_one():
    """
        Select 1 from database
    """
    sql = "SELECT * FROM stella LIMIT 2"
    results = query_db(sql)
    # print results
    return results

def test():
    # print "in test()"
    # query_db("CREATE TABLE foo(a int);")
    # sql = "CREATE FLEX TABLE product_data();"
    # sql = "DROP TABLE product_data"
    # sql = "DROP TABLE foo2"
    # sql = "CREATE TABLE foo(SKU VARCHAR(10), Name VARCHAR(80), Unit of Measure VARCHAR(10));"
    # sql = "COPY foo from LOCAL '/Users/Admin/vertica-hackathon/foo.csv'"
    # sql = "CREATE TABLE product_database(SKU VARCHAR(10), Name VARCHAR(80), Category VARCHAR(80), Unit_of_Measure VARCHAR(10), Manufacturer VARCHAR(80), Brand VARCHAR(80), Manufacturer_Code VARCHAR(20), Manufacturer_Name VARCHAR(80), Vendor VARCHAR(80), Vendor_Code VARCHAR(20), Vendor_Name VARCHAR(80), Cold_Chain BOOLEAN, UPC VARCHAR(20), NPC VARCHAR(20));"
    # sql = "COPY product_data FROM LOCAL '/Users/Admin/Downloads/Partners In Health - Product Data - Sheet1.csv' DELIMITER ',';"
    # query_db("INSERT INTO foo VALUES (1)")
    # sql = "SELECT * FROM product_data;"
    # sql = "SELECT * FROM foo"
    sql = "SELECT SKU, inventory1 from product_data where inventory1 < 100 order by inventory1 DESC, SKU ASC"
    results = query_db(sql)
    print results
    return results

# @app.teardown_appcontext
def close_connection(exception):
    # print 'in close_connection()'
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
