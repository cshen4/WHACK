from flask import Flask
from flask import request
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
    db.updateInv()

    results = db.test()
    print 'got results'
    return render_template("index.html", results=results)

@app.route('/', methods=['POST'])
def my_form_post():

    # text = request.form['text']
    status = 0
    text = request.form
    for key in text.keys():
        for value in text.getlist(key):
            # SKU = key
            # Status = value
            if value.isdigit():
                status = int(value)
                db.updateShipment(status, key)
    # processed_text = text.upper()
    # print 'got text'
    # print text_1
    # print processed_text
    results = db.test()
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run('0.0.0.0')
