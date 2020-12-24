from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from poolGame import app, socketio
import numpy as np
from cv2 import cv2
import io
import base64
from poolGame import ball_detection
import json

settings = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/livevideo')
def live_feed():
    return render_template('video-feed.html')

@socketio.on('video')
def video_process():
    pass

@socketio.on('image')
def image(data_image):
    # emit the frame back
    sid = request.sid
    heading, encoded_data = data_image.split(',')
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    frame = ball_detection.detect_coordinates(frame,settings[sid])
    _, im_arr = cv2.imencode('.png', frame)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()

    emit('response_back', { 'frame': im_bytes })

@socketio.on('settings')
def settings_variable(data):
    json_data = json.loads(data)
    sid = request.sid
    settings[sid] = json_data

@socketio.on('connect')
def connect():
    sid = request.sid
    settings[sid] = {
        "lh":60,
        "ls":0,
        "lv":0,
        "uh":84,
        "us":255,
        "uv":255,
        "min_rad":20,
        "max_rad":27,
        "sensitivity":75
    } 
    

@socketio.on('disconnect')
def disconnect():
    sid = request.sid
    if sid in settings:
        settings.pop(sid)
    print('User disconnected')
    