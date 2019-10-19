# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, current_app, make_response, send_file
from flask_api import status
import os.path
import requests
from io import BytesIO
import sys
import logging
import pathlib
import cv2
import numpy as np
import ast
import wave, array
import itertools

#Debug logger
import logging 
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(error):
    logging.exception(error)
    return jsonify({'message': 'internal server error'}), status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route("/")
def index():
    return jsonify({'message': 'Hello SpaceApps 2019!'})

@app.route("/data", methods=['GET', 'POST'])
def data():
    stream = request.files['file'].stream
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)
    canny = cv2.Canny(img,cv2.CV_64F, 50, 110)
    canny_flat = list(itertools.chain.from_iterable(canny))
    #canny_flat = canny.flatten().tolist()

    message = "{}".format(canny_flat)
    return jsonify({'data': message})

@app.route("/wav", methods=['GET', 'POST'])
def wav():
    stream = request.files['file'].stream
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)
    canny = cv2.Canny(img,cv2.CV_64F, 50, 110)
    canny_flat = list(itertools.chain.from_iterable(canny))
    #canny_flat = canny.flatten().tolist()
    logging.debug('{}'.format(canny))

    message = "{}".format(canny_flat)

    F = canny_flat
    
    # 高速逆フーリエ変換
    f = np.fft.ifft(F)

    # 実部の値のみ取り出し
    f = f.real

    # temporally file name
    filename = "test.wav"

    # save wav file
    buf = np.array(F, dtype='int64')

    w = wave.Wave_write(filename)
    w.setparams((
        1,                        # channel
        2,                        # byte width
        16000,                    # sampling rate
        len(buf),                 # number of frames
        "NONE", "not compressed"  # no compression
    ))

    w.writeframes(array.array('h', buf).tostring())
    w.close()

    path_to_file = "test.wav"

    return send_file(
        path_to_file, 
        mimetype="audio/wav", 
        as_attachment=True, 
        attachment_filename="test.wav")
