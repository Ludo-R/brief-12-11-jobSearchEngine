#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:50:37 2020

@author: randon
"""

from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run()
    
    