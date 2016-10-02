"""
    Connect to a vertica database and run queries
"""

from twilio.rest import TwilioRestClient
from flask import g
import vertica_python
import cli

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

# def make_dicts(cursor, row):
#     """
#         Turn query results into dictionaries keyed by column name
#     """
#     # print 'in make_dicts()'
#     colnames = [col[0] for col in cursor.description]
#
#     fmtrow = {}
#     for idx, value in enumerate(row):
#       fmtrow[colnames[idx]] = value
#
#     return fmtrow
#
# def get_db():
#     # print "in get_db()"
#     db = getattr(g, '_database', None)
#     # print 'succeeded getattr()'
#     if db is None:
#         # print 'db is none'
#         db = g._database = vertica_python.connect(**conn_info)
#     # print 'out of if statement'
#     return db


# def query_db1(query, args=(), one=False):
#     # print 'in query_db'
#     print query
#     cur = get_db().cursor()
#
#     try:
#         cur.execute(query, args)
#         rv = cur.fetchall()
#
#         # Turn into colname->val dict representation of tuple
#         # this isn't very efficient but will suffice for now
#         rv = [make_dicts(cur, row) for row in rv]
#     except Exception, e:
#         print e
#         rv = [{'error': e}]
#
#     cur.close()
#     return (rv[0] if rv else None) if one else rv

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
    # sql = "CREATE TABLE product_database(SKU VARCHAR(10), Name VARCHAR(100), Category VARCHAR(100), Unit_of_Measure VARCHAR(10), Manufacturer VARCHAR(100), Brand VARCHAR(100), Manufacturer_Code VARCHAR(20), Manufacturer_Name VARCHAR(100), Vendor VARCHAR(100), Vendor_Code VARCHAR(20), Vendor_Name VARCHAR(100), Cold_Chain BOOLEAN, UPC VARCHAR(20), NPC VARCHAR(20), Inventory1 int, Min1 int, Min2 int, Inventory2 int);"

    sql = "SELECT Name, SKU, inventory1, inventory2 from product_database where inventory1 > 0 and inventory2 > 0 order by inventory1 DESC, inventory2 DESC"
    results = cli.query_db(sql)
    # print results
    return results

def updateInv():
    print 'HERE'
    account_sid = "AC3af4bdae50407788d5c400e476515950"
    auth_token  = "65d12dd7f3b0100dec3f0c1e9a4eb9dd"
    client = TwilioRestClient(account_sid, auth_token)

    sms = client.sms.messages.list()

    d = cli.sku_dict()

    for x in sms:
        print x.body
        # print x.body
        if x.from_ != "+16179256605":
            count = 0
            c = ''
            for el in x.body.split():
                print x.body.split()
                print x.from_
                # print el
                if el.isdigit():
                    print count
                    count = int(el)
                if el in d:
                    print c
                    c = el
                cli.query_db("UPDATE product_database SET Inventory1 = " + str(count) + " WHERE SKU = " + "'" + c + "'; commit;")
            # client.messages.delete(x.sid)
            client.messages.create(to=x.from_, from_="+16179256605",
                                    body="You've ordered " + str(count) + " units of " + c + ". Thank you!")
        client.messages.delete(x.sid)
def updateShipment(ship, SKU):
    # print cli.query_db("SELECT Inventory1 FROM product_database WHERE SKU = " + "'" + SKU + "'; commit;" )[0]
    inv = cli.query_db("SELECT Inventory1 FROM product_database WHERE SKU = " + "'" + SKU + "'; commit;" )[0]['Inventory1']
    cli.query_db("UPDATE product_database SET Inventory1 = " + str(inv - ship) + " WHERE SKU = " + "'" + SKU + "'; commit;")

    account_sid = "AC3af4bdae50407788d5c400e476515950"
    auth_token  = "65d12dd7f3b0100dec3f0c1e9a4eb9dd"
    client = TwilioRestClient(account_sid, auth_token)

    client.messages.create(to="+16097216990", from_="+16179256605",
                            body=str(ship) + " units of " + SKU + " has been shipped!")

# @app.teardown_appcontext
def close_connection(exception):
    # print 'in close_connection()'
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
