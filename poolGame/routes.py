from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from poolGame import app, socketio


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/livevideo')
def video():
    return render_template('video-feed.html')

@socketio.on('image')
def image(data_image):
    # emit the frame back
    emit('response_back', data_image)