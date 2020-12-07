import datetime
import requests
import base64

from info import sensitive, urlist

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True

    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret

        if client_secret == None or client_id == None:
            raise Exception("You must set an ID and a Secret.")

        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_base64 = self.get_client_credentials()
        return { "Authorization": f"Basic {client_creds_base64}" }

    def get_token_data(self):
        return { "grant_type": "client_credentials" }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()

        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            return "false"

        token_response_data = (r.json())
        now = datetime.datetime.now()
        access_token = token_response_data["access_token"]
        expires_in = token_response_data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)

        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return "true"

#    def get_genres(self):
#        endpoint = 