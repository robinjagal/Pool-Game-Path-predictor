from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from poolGame import app, socketio
import numpy as np
from cv2 import cv2
import io
import base64



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/livevideo')
def video():
    return render_template('video-feed.html')

@socketio.on('image')
def image(data_image):
    
    # emit the frame back
    encoded_data = data_image.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    emit('response_back', data_image)
    