import cv2
import numpy as np
import json
import requests
import secrets
import string
import logging
import os
import pdb

from skimage import io
from processes import imgproc
from apis import spotify
from info import sensitive, urlist
from urllib.parse import urlencode

from flask import (Flask,
                   abort,
                   make_response,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)

IMAGE_DOWNSCALE = 20

processor = Flask(__name__)
processor.secret_key = sensitive.SECRET_KEY
spotify_api = spotify.SpotifyAPI()

@processor.route('/')
def index():
    if session.get('tokens') is not None and session.get('tokens').get('access_token') is not None:
        return render_template('home.html')
    else:
        return render_template('login.html')


# Spotify routes
@processor.route('/login', methods=['GET'])
def login():
    return (spotify_api.get_user_permission())

@processor.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    stored_state = request.cookies.get('spotify_auth_state')

    response = spotify_api.get_auth_token(code)
    response_data = response.json()

    if response_data.get('error') is not None or response.status_code != 200:
        processor.logger.error('Failed to receive token')
        abort(response.status_code)

    session['tokens'] = {
        'access_token': response_data.get('access_token'),
        'refresh_token': response_data.get('refresh_token')
    }

    return redirect('/')

@processor.route('/getSongs', methods=['POST'])
def get_songs():
    if request.method == 'POST':
        color = request.form['color']
        audio_features = request.form['audioFeatures']
        code = session['tokens'].get('access_token')
        refresh = session['tokens'].get('refresh_token')

        songs = spotify_api.get_related_tracks(code, audio_features)
        #pdb.set_trace()

        return render_template('tracklist.html', result=songs, color=color)

    return "Error"

# Image Processing routes
@processor.route('/getColor', methods=['POST'])
def get_dominant_color():
    if request.method == 'POST':
        image = io.imread(request.files['userfile'])[:, :, :-1]

        width = int(image.shape[1] * IMAGE_DOWNSCALE / 100)
        height = int(image.shape[0] * IMAGE_DOWNSCALE / 100)
        dim = (width, height)

        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        dominant = imgproc.get_dominant_color(image)

        return (dominant)

if __name__ == '__main__':
    processor.debug = True
    processor.run()