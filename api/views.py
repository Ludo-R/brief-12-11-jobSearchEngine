#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:50:37 2020

@author: randon
"""

from flask import Flask, render_template, url_for, request
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["jobsearchengine"]
collection = db["testjob"]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST'])
def result():
    r = request.form.get("research")
    a = db.testjob.find({"query":r}).sort([("pubDate", -1)])
    
    return render_template('result.html', resultat = r, job= a)

if __name__ == "__main__":
    app.run()
    

    