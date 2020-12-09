import requests
import string
import secrets

from info import sensitive, urlist
from flask import make_response, redirect
from urllib.parse import urlencode

import pdb

class SpotifyAPI(object):
    client_id = None
    client_secret = None
    user_top_genres = None
    user_id = None

    def __init__(self):
        self.client_id = sensitive.CLIENT_ID
        self.client_secret = sensitive.CLIENT_SECRET

    def get_user_permission(self):
         state = ''.join(
             secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
         )

         scope = "user-top-read user-library-read playlist-modify-public playlist-modify-private user-read-private user-read-email"
         payload = {
             'client_id': self.client_id,
             'response_type': 'code',
             'redirect_uri': urlist.REDIRECT_URI,
             'scope': scope
         }

         response = make_response(redirect(f'{urlist.AUTH_URL}/?{urlencode(payload)}'))
         response.set_cookie('spotify_auth_state', state)

         return response

    def get_auth_token(self, code):
         payload = {
             'grant_type': 'authorization_code',
             'code': code,
             'redirect_uri': urlist.REDIRECT_URI
         }

         response = requests.post(urlist.TOKEN_URL, auth=(self.client_id, self.client_secret), data=payload)
         response_data = response.json()
         self.get_top_genres(response_data.get('access_token'))

         return response

    def refresh_token(self, refresh_token):
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        result = requests.post(urlist.TOKEN_URL, auth=(self.client_id, self.client_secret), data=payload, headers=headers)
        return result.json()

    def get_user_id(self, code):
        headers = { 'Authorization': f'Bearer {code}' }
        endpoint = f'{urlist.USER_URL}'
        response = request.get(endpoint, headers=headers).json()

        if response.get('error') is not None and response.get('error').get('status') == 401:
            return response

        self.user_id = request.get(endpoint, headers=headers).json().get('id')

    def get_top_genres(self, code):
        headers = { 'Authorization': f'Bearer {code}' }
        params = {
            'limit': 5,
            'time_range': 'short_term'
        }

        endpoint = f'{urlist.TOP_ARTISTS}/?{urlencode(params)}'
        artists = requests.get(endpoint, headers=headers).json()

        if artists.get('error') is not None and artists.get('error').get('status') == 401:
            return artists

        artists = artists.get('items')
        genres = []

        for artist in artists:
            artist_genres = artist.get('genres')
            if artist_genres:
                genres.append(artist_genres[0])

        genres = list(dict.fromkeys(genres))
        self.user_top_genres = genres

    def get_related_tracks(self, code, audio_features):
        if self.user_top_genres is None:
            self.get_top_genres(code)

        genre_param = ""
        for genre in self.user_top_genres:
            genre_param += genre + ","

        headers = { 'Authorization': f'Bearer {code}' }
        params = {
            'seed_genres': genre_param[:-1],
            'limit': 9,
            'max_popularity': 40
        }

        endpoint = f'{urlist.RELATED_TRACKS}?{urlencode(params)}&{audio_features}'
        tracks = requests.get(endpoint, headers=headers).json()

        if tracks.get('error') is not None and artists.get('error').get('status') == 401:
            return tracks

        return tracks