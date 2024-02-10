from PyQt5 import QtCore, QtMultimedia
from extra.other.func_gui import *
import extra.other.func_set_change_return_data
import json
import os


def change_repeat(self):
    if self.is_repeat:
        self.is_repeat = False
        self.repeat_bttn.setText(self.translated_elements[19])
    else:
        self.is_repeat = True
        self.repeat_bttn.setText('1')

def set_track_names(self):
    if type(self.json_data['Playlists'][self.current_track_playlist]) == list:
        self.current_track_name = self.json_data['Playlists'][self.current_track_playlist][0]
        self.current_track = self.json_data['Playlists'][self.current_track_playlist][0]
        extra.other.func_set_change_return_data.pause_or_resume_w_args(self)
    elif type(self.json_data['Playlists'][self.current_track_playlist]) == dict:
        self.current_track_name = list(
            self.json_data['Playlists'][self.current_track_playlist].keys())[0]
        self.current_track = self.json_data['Playlists'][self.current_track_playlist][self.current_track_name]
        extra.other.func_set_change_return_data.pause_or_resume_w_args(self)

def switch_playlist(self, action):
    items = [self.playlists.item(x).text()
                for x in range(self.playlists.count())]
    for i in range(len(items)):
        if items[i] == self.current_track_playlist:
            try:
                if action == 'next':
                    next_playlist = items[i + 1]
                elif action == 'prev':
                    next_playlist = items[i - 1]
            except IndexError:
                next_playlist = items[0]
                self.logs_listwidget.addItem('IndexError')
    set_track_names(self)

def swith_track(self, action):
    if self.current_track != '':
        if self.current_track_playlist == 'Local':
            try:
                self.json_data['Playlists']['Local'] = []
                self.playlists_data = os.listdir('files')
                for track in self.playlists_data:
                    self.json_data['Playlists']['Local'].append(
                        'files/' + track)
                if action == 'next':
                    self.current_track = self.json_data['Playlists'][self.current_track_playlist][
                        self.json_data['Playlists'][self.current_track_playlist].index(self.current_track_name) + 1]
                elif action == 'prev':
                    self.current_track = self.json_data['Playlists'][self.current_track_playlist][
                        self.json_data['Playlists'][self.current_track_playlist].index(self.current_track_name) - 1] 

                self.current_track_name = self.current_track
                extra.other.func_set_change_return_data.pause_or_resume_w_args(self)

            # If last track in playlist - select first track
            except IndexError:
                self.logs_listwidget.addItem('IndexError')
                if action == 'next':
                    self.current_track = self.json_data['Playlists'][self.current_track_playlist][0]
                elif action == 'prev':
                    self.current_track = self.json_data['Playlists'][self.current_track_playlist][-1]

                self.current_track_name = self.current_track
                extra.other.func_set_change_return_data.pause_or_resume_w_args(self)
        else:
            try:
                self.playlist_tracks_values = list(
                    self.json_data['Playlists'][self.current_track_playlist].values())
                if action == 'next':
                    self.current_track = self.playlist_tracks_values[self.playlist_tracks_values.index(
                        self.current_track) + 1]
                elif action == 'prev':
                    print(self.playlist_tracks_values[self.playlist_tracks_values.index(self.current_track) - 1])
                    self.current_track = self.playlist_tracks_values[self.playlist_tracks_values.index(self.current_track) - 1]                        
                for k, v in self.json_data['Playlists'][self.current_track_playlist].items():
                    if v == self.current_track:
                        self.current_track_name = k
                        break
                print(self.current_track)
                extra.other.func_set_change_return_data.pause_or_resume_w_args(self)

            # If last track in playlist - select first track
            except IndexError:
                self.logs_listwidget.addItem('IndexError')
                self.playlist_tracks_values = list(
                    self.json_data['Playlists'][self.current_track_playlist].values())
                if action == 'next':
                    self.current_track = self.playlist_tracks_values[0]
                elif action == 'prev':
                    self.current_track = self.playlist_tracks_values[-1]
                for k, v in self.json_data['Playlists'][self.current_track_playlist].items():
                    if v == self.current_track:
                        self.current_track_name = k
                        break
                extra.other.func_set_change_return_data.pause_or_resume_w_args(self)
            except ValueError:
                pause(self)
            except KeyError as ke:
                self.logs_listwidget.addItem('KeyError')
    try:
        select_element(self)
    except Exception as exc:
        print(exc)        

def play(self, song):
    self.play_bttn.setText('Pause')
    if self.song == song and self.player.isAudioAvailable() == False:
        pass
    else:
        if self.its_online_track:
            if self.current_track_name in list(self.online_tracks_data.keys()):
                self.player.setMedia(self.online_tracks_data[self.current_track_name])
            else:
                media_data = QtMultimedia.QMediaContent(QtCore.QUrl(song))
                self.player.setMedia(media_data)
                self.song = song
                self.online_tracks_data[self.current_track_name] = media_data
        else:
            if self.player.isAudioAvailable() == False:
                self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl(song)))
                self.song = song
            if self.song == song:
                pass
            else:
                self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl(song)))
                self.song = song

    self.player.play()
    self.Play_Pause = False

def pause(self):
    self.play_bttn.setText('Play')
    self.player.pause()
    self.Play_Pause = True

def pause_or_resume(self):
    # If track selected
    if self.current_track != '':
        self.track_name_lbl.setText(self.current_track_name)
        if self.first_play:
            # Change statistic
            temp_track_name = self.current_track_name.split('/')
            if temp_track_name[0] == 'files':
                if temp_track_name[1].split('.mp3')[-1] == '':
                    temp_track_name = temp_track_name[1]
                    temp_track_name = temp_track_name[:-4]
                else:
                    temp_track_name = temp_track_name[1]
            else:
                temp_track_name = self.current_track_name
            if temp_track_name in self.json_data['Statistic']['amount_plays']:
                self.json_data['Statistic']['amount_plays'][temp_track_name] += 1
                with open('extra/json/data.json', 'w', encoding='utf-8') as f:
                    json.dump(self.json_data, f, indent=4,
                                ensure_ascii=False)
            else:
                self.json_data['Statistic']['amount_plays'][temp_track_name] = 1
                with open('extra/json/data.json', 'w', encoding='utf-8') as f:
                    json.dump(self.json_data, f, indent=4,
                                ensure_ascii=False)

            self.first_play = False
            print('play:\t' + self.current_track)
            play(self, self.current_track)
        else:
            if self.Play_Pause == False:
                pause(self)
            else:
                play(self, self.current_track)