import requests
import os


class Track:
    def __init__(self, title, cover, album, artists):
        self.title = title
        self.cover = cover
        self.album = album
        self.artists = artists
        self.youtube_url = None

        self.imgdir = "C:\\Users\\pacot\\PycharmProjects\\Spotipython\\outputs\\images"

        self.handle_artists()
        self.handle_name()
        self.download_image_cover()

    def handle_artists(self): #Put only the "name" key inside of self.artists
        if len(self.artists) > 1:
            artists = []
            for artist in self.artists:
                artists.append(artist["name"])
            self.artists = artists
        else:
            self.artists = [self.artists[0]["name"]]

        print(self.artists)

    def handle_name(self): #Replace all windows forbidden characters
        self.title = self.title.replace("?", "")
        self.title = self.title.replace(":", "")
        self.title = self.title.replace("<", "")
        self.title = self.title.replace(">", "")
        self.title = self.title.replace("|", "")
        self.title = self.title.replace("/", "")
        self.title = self.title.replace("*", "")
        self.title = self.title.replace("\\", "")


    def download_image_cover(self): #Downloads the album cover image using requests.get
        response = requests.get(self.cover)
        print(self.title)
        img_path = f"{self.imgdir}\\{self.title}.jpg"
        with open(img_path, "wb") as f:
            f.write(response.content)
        self.cover = img_path

    def edit_values(self, values): #Take new values edited by the user. Called by LowerFrame in tela.py
        os.rename(f"{self.imgdir}\\{self.title}.jpg", f"{self.imgdir}\\{values[0][:-1]}.jpg")
        self.title = values[0][:-1]
        self.album = values[1][:-1]
        self.artists = self.string_to_list(values[2])

    def string_to_list(self, s): #Take the artists string and transform it to a list
        s = s.replace("{", "")
        s = s.replace("}", "")
        s = s[:-1]
        return s.split(", ")

    def __del__(self): #Deletes the object and the cover image
        os.remove(f"{self.imgdir}\\{self.title}.jpg")
