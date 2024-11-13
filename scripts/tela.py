import customtkinter
from PIL import Image
import webbrowser


# Upper frame of the screen. Manages the input link, the "Search" button, and the "Download All" button
class UpperFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.input = customtkinter.CTkEntry(self, placeholder_text="Coloque o link aqui", width=600)
        self.input.grid(row=0, column=0, padx=10, pady=15, sticky="n")

        self.search = customtkinter.CTkButton(self, text="Procurar", command=master.search, width=70)
        self.search.grid(row=0, column=1, padx=5, pady=15, sticky="n")

        self.download_all = customtkinter.CTkButton(self, text="Baixar", command=lambda t=-1: master.download(t),
                                                    width=70)
        self.download_all.grid(row=0, column=2, padx=5, pady=15, sticky="n")


# Lower frame of the screen. Manages all the tracks, showing one-by-one with image and all the data
class LowerFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, tracks):
        super().__init__(master)
        self.master = master
        self.track_frames = []
        self.frames = []
        self.top_level_window = None

        for i, track in enumerate(tracks):
            frame = customtkinter.CTkFrame(master=self, width=750, height=60)

            img = customtkinter.CTkImage(Image.open(track.cover), size=(100, 100))
            edit_img = customtkinter.CTkImage(
                Image.open("C:\\Users\\pacot\\PycharmProjects\\Spotipython\\src\\editIcon.png"),
                size=(15, 15))
            download_img = customtkinter.CTkImage(
                Image.open("C:\\Users\\pacot\\PycharmProjects\\Spotipython\\src\\downloadIcon.png"),
                size=(15, 15))
            search_img = customtkinter.CTkImage(
                Image.open("C:\\Users\\pacot\\PycharmProjects\\Spotipython\\src\\searchIcon.png"),
                size=(15, 15))
            delete_img = customtkinter.CTkImage(
                Image.open("C:\\Users\\pacot\\PycharmProjects\\Spotipython\\src\\deleteIcon.png"),
                size=(15, 15))

            image_label = customtkinter.CTkLabel(frame, image=img, text="")
            image_label.grid(row=0, column=0, padx=10, pady=5)

            info = customtkinter.CTkFrame(master=frame, width=670, height=60)
            info.grid_rowconfigure(0, weight=1)
            info.grid_rowconfigure(1, weight=1)

            entries = customtkinter.CTkFrame(master=info, width=670, height=60)

            title_entry = customtkinter.CTkTextbox(entries, wrap="none", width=290, height=30)
            title_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
            title_entry.insert("0.0", track.title)
            album_entry = customtkinter.CTkTextbox(entries, wrap="none", width=290, height=30)
            album_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
            album_entry.insert("0.0", track.album)

            buttons = customtkinter.CTkFrame(master=info, width=670, height=60)
            buttons.grid_rowconfigure(0, weight=1)

            artists_entry = customtkinter.CTkTextbox(buttons, wrap="none", width=430, height=30)
            artists_entry.grid(row=0, column=0, padx=5, pady=5, sticky="s")
            artists_entry.insert("0.0", track.artists)

            edit_button = customtkinter.CTkButton(master=buttons, text="",
                                                  command=lambda t=(track, i): self.edit_track(t),
                                                  image=edit_img, fg_color="transparent", width=25)
            edit_button.grid(row=0, column=1, padx=5, pady=5)
            download_button = customtkinter.CTkButton(master=buttons, text="", command=lambda t=track: self.download_track(t),
                                                      image=download_img, fg_color="transparent", width=25)
            download_button.grid(row=0, column=2, padx=5, pady=5)
            search_button = customtkinter.CTkButton(master=buttons, text="",
                                                    command=lambda t=(track, i): self.search_track(t),
                                                    image=search_img, fg_color="transparent", width=25)
            search_button.grid(row=0, column=3, padx=5, pady=5)
            delete_button = customtkinter.CTkButton(master=buttons, text="",
                                                    command=lambda t=(track, i): self.delete_track(t),
                                                    image=delete_img, fg_color="transparent", width=25)
            delete_button.grid(row=0, column=4, padx=5, pady=5)

            self.track_frames.append([
                title_entry, album_entry, artists_entry
            ])
            self.frames.append(frame)

            frame.grid(row=i, column=0, padx=10, pady=5, sticky="n")
            info.grid(row=0, column=1, padx=0, pady=5)
            entries.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            buttons.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    def edit_track(self, track):  # track = (Track Object, index of the buttons)
        track[0].edit_values(values=[
            self.track_frames[track[1]][0].get("0.0", "end"),
            self.track_frames[track[1]][1].get("0.0", "end"),
            self.track_frames[track[1]][2].get("0.0", "end")
        ])

    def download_track(self, t):
        self.master.download(t)

    def search_track(self, track):
        webbrowser.open_new_tab(track[0].youtube_url)

    def delete_track(self, track):
        self.frames[track[1]].destroy()
        self.master.delete(track[0])


class Screen(customtkinter.CTk):  # Main Screen, creates all the app GUI, managing every component
    def __init__(self, context):
        super().__init__()

        self.context = context  # Class Main from main.py
        self.input = ""  # Input link from the user

        self.title = "Tela Principal"
        self.geometry("790x790")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.upper_frame = UpperFrame(self)
        self.upper_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    def search(self):
        self.context.input_received(self.upper_frame.input.get())

    def download(self, t):
        self.context.download_tracks(t)

    def delete(self, t):
        self.context.delete_track(t)

    def draw_tracks(self, tracks):
        self.lower_frame = LowerFrame(self, tracks)
        self.lower_frame.configure(width=760, height=640)
        self.lower_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")
