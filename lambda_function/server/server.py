from flask import Flask
from flask import render_template

app = Flask(__name__)
# app.configselffrom_object(__name__)

import db_model as db
import json

from datetime import date
from datetime import timedelta

@app.route("/")
def index():

    # results = db.select_one()
    results = db.test()
    print 'got results'
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run('0.0.0.0')