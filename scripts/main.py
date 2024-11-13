from tela import Screen
from spotify_api import Spotify
from spotify_track import Track
from youtube_search import YoutubeSearch
from downloader import Downloader

class Main:
    def __init__(self):
        self.screen = Screen(context=self)
        self.spotify = Spotify()
        self.youtube = YoutubeSearch()
        self.downloader = Downloader()

        self.spotify_results = None
        self.spotify_tracks = []

        self.screen.mainloop()

    def input_received(self, link): #User input received. This function is only called by class Screen in tela.py
        if link.find("spotify") != -1:
            self.spotify_results = self.spotify.input(link)
            self.spotify_reader()

        elif link.find("youtube") != -1:
            pass

    #See if it's a playlist or track. Creates Track objects with all the important stuff, stored in self.spotify_tracks
    def spotify_reader(self):
        if "items" in self.spotify_results: #The "items" key is only available in a playlist
            for item in self.spotify_results["items"]:
                self.spotify_tracks.append(Track(
                    title=item["track"]["name"],
                    cover=item["track"]["album"]["images"][0]["url"],
                    album=item["track"]["album"]["name"],
                    artists=item["track"]["artists"]
                ))
        #If it is a track, the "type" value will be "track"
        elif "type" in self.spotify_results and self.spotify_results["type"] == "track":
            self.spotify_tracks.append(Track(
                title=self.spotify_results["name"],
                cover=self.spotify_results["album"]["images"][0]["url"],
                album=self.spotify_results["album"]["name"],
                artists=self.spotify_results["artists"]
            ))

        self.youtube_searcher()

    def youtube_searcher(self): #Finds the track in YouTube using YoutubeSearch from youtube_search.py
        for track in self.spotify_tracks:
            track.youtube_url = self.youtube.getURL(track)

        self.screen.draw_tracks(tracks=self.spotify_tracks) #With everything OK, show the tracks to user

    #Receives the requested tracks for download. "requested" can be -1 for all tracks, or the specific track object
    def download_tracks(self, requested):
        if requested == -1:
            for track in self.spotify_tracks:
                self.downloader.download_track(track)
        else:
            index = self.spotify_tracks.index(requested)
            self.downloader.download_track(requested)

    def delete_track(self, track):
        track.__del__()
        self.spotify_tracks.pop(self.spotify_tracks.index(track))



main = Main()