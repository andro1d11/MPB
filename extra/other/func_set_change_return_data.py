from PyQt5.QtWidgets import QFileDialog
from extra.other.parsers import *
from extra.other.func_other import *
from extra.other.func_playlists import *
from extra.other.parsers import *
from init_parsers import init_parsers
from datetime import timedelta
from copy import deepcopy
import pyglet
import time
import extra.other.func_player_control


def search_for_playlist(self):
    if self.action == 'playlist':
        for i in range(self.tracks_area.count()):
            item = self.tracks_area.item(i)
            if self.find_track_input.text().lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

def update_recomendations(self):
    # Popularity of tracks fok week
    popular_tracks_temp = {}
    result = []
    unsorted_popular_tracks_temp = self.json_data['Statistic']['amount_plays']
    sorted_popular_tracks_temp_keys = sorted(
        unsorted_popular_tracks_temp, key=unsorted_popular_tracks_temp.get, reverse=True)
    for w in sorted_popular_tracks_temp_keys:
        popular_tracks_temp[w] = unsorted_popular_tracks_temp[w]
    for i in range(3):
        result.append(list(popular_tracks_temp.keys())[i])

def update_json_data(self):
    temp = {}
    current_playlist = self.playlists.currentItem().text()
    if current_playlist != 'Local':
        for item in range(self.tracks_area.count()):
            print(self.tracks_area.count())
            temp_track_name = self.tracks_area.item(item).text()
            if temp_track_name == '':
                continue
            temp[temp_track_name] = self.json_data['Playlists'][current_playlist][temp_track_name]
        self.json_data['Playlists'][current_playlist] = temp
        with open('extra/json/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_without_local_playlist(self),
                        f, indent=4, ensure_ascii=False)

# Return M:S from track timestamp with qmediaplayer
def return_human_time_from_track_pyqt(self):
    try:
        ts = self.player.duration()
        if ts >= 3600000:
            return ts, time.strftime('%H:%M:%S', time.gmtime(timedelta(milliseconds=ts).seconds))
        else:
            return ts, time.strftime('%M:%S', time.gmtime(timedelta(milliseconds=ts).seconds))
    except Exception as exc:
        print(exc)
        self.logs_listwidget.addItem('Error')
        return 0, '0:00'

# Return M:S from track timestamp with pyglet
def return_human_time_from_track_pyglet(self, track_file):
    try:
        ts = pyglet.media.load(track_file).duration
        return ts * 1000, time.strftime('%M:%S', time.gmtime(ts))
    except Exception as exc:
        self.logs_listwidget.addItem('Error')
        return 0, '0:00'

# Returns all playlists that contain the title of the track.
def find_track_in_playlists(self, trcks):
    playlists = []
    self.temp_data = data_without_local_playlist(self)
    self.temp_data['Playlists'].pop('Local')
    for playlist in self.temp_data['Playlists'].keys():
        for track in self.temp_data['Playlists'][playlist].values():
            if track in trcks:
                playlists.append(playlist)
    return playlists

def data_without_local_playlist(self):
    self.temp_data = deepcopy(self.json_data)
    self.temp_data['Playlists']['Local'] = []
    return self.temp_data

def return_clear_track_name(self, track_name):
    return track_name.split('files/')[1].split('.mp3')[0]

# Additional arguments for pause_or_resume()
def pause_or_resume_w_args(self):
    self.Play_Pause = True
    self.first_play = True

    set_track_data(self)
    extra.other.func_player_control.pause_or_resume(self)

    self.track_time_data = None
    self.track_time = None
    if self.full_discord_activities:
        self.rpc_client.update(f'{self.current_track_name}', '00:00')

def set_temp_tracks(self):
    if self.action == 'playlist':
        if self.tracks_area.selectedItems() != []:
            self.temp_tracks = []
            for i in self.tracks_area.selectedItems():
                self.temp_tracks.append(i.text())

def redact_text(self, text, num):
    text = list(text)
    for i in range(len(text)):
        if i % num == 0:
            for j in range(i):
                if j >= 10:
                    text[i - j] = f'{text[i - j]}-\n'
                    break
                elif text[i - j] == ' ':
                    text[i - j] = '\n'
                    break
    text = ''.join(text)
    return text

def set_track_data(self):
    self.track_time_data = return_human_time_from_track_pyqt(self)
    if self.track_time_data[0] >= 3600000:
        self.track_bigger_than_hour = True
    else:
        self.track_bigger_than_hour = False
    self.track_time = self.track_time_data[0]
    self.all_track_time.setText(self.track_time_data[1])
    self.track_slider.setMaximum(int(self.track_time))
    if not self.first_play:
        self.track_slider.setValue(0)

def open_tracks_file_Dialog(self):
    self.tracks_file_name = QFileDialog.getOpenFileName(
        self, "Open tracks file", "", "Text Files (*.txt)")
    self.download_tracks_from_file(self.tracks_file_name)

def rate_track(self):
    self.rating[self.rate_track_name_lbl.text()] = int(self.rate_result)

# If button under track area (track_area_action_bttn) clicked
def select_action(self):
    if self.action == 'download':
        parse_track(self)
    elif self.action == 'playlist':
        delete_track_form_playlist(self)
    
    # Command prompt
    elif self.action == 'connect':
        global net_mode, parsers, parser_lyrics, parser_youtube, parser_lastfm, parsers_status
        if self.find_track_input.text() == '!mpb restart_parsers':
            self.logs_listwidget.addItem('COMMAND restart_parsers')
            parsers = init_parsers(debug=self.debug_mode)
            parsers.start_threads()
            parser_lyrics, parser_youtube, parser_lastfm = parsers.result

            if False in [parser_youtube.connection, parser_lyrics.connection, parser_lastfm.connection]:
                net_mode = 1
                try:
                    parser_lastfm.quit_webdriver()
                except:
                    pass
            else:
                net_mode = 0

            if net_mode == 0:
                self.parse_tracks_thread = parse_tracks_urls_thread(
                    mainWindow=self)
                self.download_track_thread = download_track_thread(mainWindow=self)
                self.download_playlist_thread = download_playlist_thread(
                    mainWindow=self)
                self.get_tracks_to_lyrics_thread = get_tracks_to_lyrics_thread(
                    mainWindow=self)
                self.get_lyrics_thread = get_lyrics_thread(mainWindow=self)

            self.logs_listwidget.addItem('DONE!')
            parsers_status = f'YouTube:{parser_youtube.connection}\nLyrics:{parser_lyrics.connection}\nLastFm:{parser_lastfm.connection}'
            self.logs_listwidget.addItem(parsers_status)

        elif self.find_track_input.text() == '!mpb clear_queue':
            self.queue = []
            self.queue_listwidget.clear()
            self.logs_listwidget.addItem('Queue has been cleared')