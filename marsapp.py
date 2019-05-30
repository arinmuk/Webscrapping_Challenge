from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import textwrap
import pymongo
import datetime as datetime
#mongo = PyMongo(app, uri="mongodb+srv://arinmuk:amarji123!@cluster0-omshy.mongodb.net/test?retryWrites=true")

app = Flask(__name__)
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")
mongo = PyMongo(app, uri="mongodb+srv://arinmuk:amarji123!@cluster0-omshy.mongodb.net/test?retryWrites=true")
mars_data={}
#conn = 'mongodb://localhost:27017'
conn ='mongodb+srv://arinmuk:amarji123!@cluster0-omshy.mongodb.net/test?retryWrites=true'
client = pymongo.MongoClient(conn)
db = client.mars_data
mars_scrape_col = db.mars_scrape.find()


@app.route('/')
def index():
    marsdata = db.mars_scrape.find_one()
    return render_template('index.html', marsdata=marsdata)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars_scrape
    data = scrape_mars.scrape()
    mars.update_one(
        {},
        {"$set":data},
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
