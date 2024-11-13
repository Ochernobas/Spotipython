from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


class Spotify:
    def __init__(self):
        load_dotenv()

        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.texto = ""

    #Get access token for Spotify's API
    #Functions "getToken" and "get_auth_header" copied from Tech with Tim
    #Original code - https://www.youtube.com/watch?v=WAmEZBEeNmg
    def getToken(self):
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]

        return token

    def get_auth_header(self, token):
        return {"Authorization": "Bearer " + token}

    #Search for a playlist using the id
    def search_for_playlist(self, id):
        url = f"https://api.spotify.com/v1/playlists/{id}"

        token = self.getToken()
        headers = self.get_auth_header(token)

        result = get(url, headers=headers)
        json_result = json.loads(result.content)

        return json_result["tracks"]

    #Search for a music using the id
    def search_for_music(self, id):
        url = f"https://api.spotify.com/v1/tracks/{id}"

        token = self.getToken()
        headers = self.get_auth_header(token)

        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result

    #Main function, decides if the user wants a music or playlist, then searches it
    def input(self, url):
        if url.find("playlist") != -1:
            return self.search_for_playlist(url.split("playlist/")[1].split("?")[0])
        elif url.find("track") != -1:
            return self.search_for_music(url.split("track/")[1].split("?")[0])
        else:
            return -1