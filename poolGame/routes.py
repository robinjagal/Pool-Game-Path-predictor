from flask import Flask, render_template
from poolGame import app

@app.route('/')
def home():
    return render_template('index.html')
