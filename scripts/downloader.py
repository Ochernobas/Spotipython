from pytubefix import YouTube
from pytubefix.cli import on_progress
import subprocess
import os
import music_tag


class Downloader: #Class responsible for downloading, converting and tagging each track
    def __init__(self):
        pass

    def download_track(self, track): #Uses pytubefix to donwload track. Filename is the track title
        path = "C:\\Users\\pacot\\PycharmProjects\\Spotipython\\outputs\\musics"

        url = track.youtube_url

        yt = YouTube(url, on_progress_callback=on_progress, use_oauth=True)
        yt.title = track.title

        ys = yt.streams.get_lowest_resolution()
        ys.download(output_path=path)

        self.convert_track(path=f"{path}\\{yt.title}.mp4", track=track)

        os.remove(f"{path}\\{yt.title}.mp4")

        self.tag_track(path=f"{path}\\{track.title}.mp3", track=track)

    def convert_track(self, path, track): #Uses FFmpeg to convert from mp3 to mp4
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", path,
            "-vn",
            "-acodec", "libmp3lame",
            "-ab", "192k",
            "-ar", "44100",
            "-y",
            f"C:\\Users\\pacot\\PycharmProjects\\Spotipython\\outputs\\musics\\{track.title}.mp3"
        ]

        try:
            subprocess.run(ffmpeg_cmd, capture_output=True)
        except:
            print("Ocorreu um erro relacionado ao FFMPEG")

    def tag_track(self, path, track): #Uses music_tag to edit tags for each track
        img_dir = "C:\\Users\\pacot\\PycharmProjects\\Spotipython\\outputs\\images"
        f = music_tag.load_file(path)
        s = ""

        f["title"] = track.title
        f["album"] = track.album

        if len(track.artists) < 2:
            f["artist"] = track.artists[0]
        else:
            for i, artist in enumerate(track.artists):
                if i == len(track.artists) - 1:
                    s = s + artist
                else:
                    s = s + artist + "; "
            f["artist"] = s

        with open(f"{img_dir}\\{track.title}.jpg", "rb") as img_in:
            f["artwork"] = img_in.read()

        os.remove(f"{img_dir}\\{track.title}.jpg")

        f.save()
