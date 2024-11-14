from youtubesearchpython import VideosSearch

class YoutubeSearch:
    def __init__(self):
        pass

    def getURL(self, track):
        artists = ""
        for artist in track.artists:
            artists = artists + ", " + artist

        q = f"{track.title} (Official Audio) {artists}"

        result = VideosSearch(q, limit=1).result()
        url = result["result"][0]["link"]
        print(q)
        return url