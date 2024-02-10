from extra.other.parsers import *
import extra.other.func_playlists
import threading
import os


# Connect external device
def accept_connection(self):
    self.server.listen(1)
    while self.is_waiting_connect:
        user_socket, address = self.server.accept()
        break
    try:
        self.logs_listwidget.addItem('Connected')
        while self.is_waiting_connect:
            try:
                received_data = user_socket.recv(1024).decode().split('/')
            except OSError:
                self.logs_listwidget.addItem('OSError')
                user_socket, address = self.server.accept()
                received_data = user_socket.recv(1024).decode().split('/')
                continue
            prefix = received_data[0]
            try:
                if prefix == 'sc':
                    received_code = received_data[1]
                    if received_code != str(self.secret_code):
                        user_socket.close()
                        self.logs_listwidget.addItem('Connection reset')
                elif prefix == 'pr':
                    self.pause_or_resume()
                elif prefix == 'nt':
                    self.swith_track('next')
                elif prefix == 'pt':
                    self.swith_track('prev')
                elif prefix == 'np':
                    self.switch_playlist('next')
                elif prefix == 'pp':
                    self.switch_playlist('prev')
                elif prefix == 'vr':
                    self.volume_slider.setValue(int(received_data[1]))
                elif prefix == 'ce':
                    self.logs_listwidget.addItem('Connection reset')
                    user_socket.close()
            except:
                pass

    except ConnectionResetError:
        self.logs_listwidget.addItem('ConnectionResetError')
        user_socket.close()

def find_tracks_to_lyrics(self):
    if self.action == 'lyrics':
        self.track_to_lyrics_temp = self.find_track_input.text()
        if self.track_to_lyrics_temp != '' and self.track_to_lyrics_temp.replace(' ', '') != '':
            self.get_tracks_to_lyrics_thread.stop_search = 0
            self.get_tracks_to_lyrics_thread.start()
    else:
        self.action = 'download'
        self.track_area_action_bttn.setText(self.translated_elements[11])
        self.tracks_area.setStyleSheet(self.tracks_area_stylesheets)
        self.tracks_area.show()
        self.parse_tracks_thread.start()

def parse_track_only_url(self):
    try:
        song_name = self.parser_youtube.get_title(self.find_track_input.text())
        url = self.find_track_input.text()
        img_url = None
        self.queue_listwidget.addItem(song_name)
        self.queue.append(
            {'song_name': song_name, 'url': url, 'img_url': img_url})
        self.song_name = None
        if self.is_downloading_now == False:
            self.download_track_thread.start()
    except Exception as exc:
        self.logs_listwidget.addItem(str(exc))

def save_for_online(self):
    self.logs_listwidget.addItem('Please, wait')
    song_name = self.tracks_area.currentItem().text()
    url = self.urls[song_name][0]

    extra.other.func_playlists.add_track_to_json(self, 'Downloads', song_name, f'ONLINE_TRACK {url}')
    self.logs_listwidget.addItem(f'Track "{song_name}" was added. Check "Downloads" playlist')

def parse_track(self):
    try:
        song_name = self.tracks_area.currentItem().text()
        url = self.urls[song_name][0]
        img_url = self.urls[song_name][1]
        self.queue_listwidget.addItem(song_name)
        self.queue.append(
            {'song_name': song_name, 'url': url, 'img_url': img_url})
        if not self.is_downloading_now:
            self.download_track_thread.start()
    except Exception as exc:
        self.logs_listwidget.addItem(str(exc))

def download_tracks_from_file(self, fpath):
    try:
        with open(fpath[0], 'r', encoding='utf-8') as f:
            tracks = f.read().split('\n')
        tracks = list(filter(lambda x: x != "", tracks))
        self.download_tracks_from_file_thread = download_tracks_from_file_thread(
            mainWindow=self, tracks=tracks)
        self.download_tracks_from_file_thread.run()
    except FileNotFoundError:
        self.logs_listwidget.addItem('FileNotFoundError')

def download_playlist(self):
    self.download_playlist_thread.run()

def open_settings(self):
    nt = threading.Thread(target=lambda: os.system(
        "notepad.exe extra/json/config.json"))
    nt.start()