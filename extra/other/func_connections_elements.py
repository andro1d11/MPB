from PyQt5 import QtGui
from extra.other.func_set_change_return_data import *
from extra.other.func_player_control import *
import time
import random
import json


# Permanent track slider movement
def play_mode(self):
    if self.Play_Pause == False:
        if not self.track_bigger_than_hour:
            str_time = time.strftime("%M:%S", time.gmtime(
                self.track_slider.value() / 1000))
        else:
            str_time = time.strftime("%H:%M:%S", time.gmtime(
                self.track_slider.value() / 1000))                
        self.current_track_time.setText(str_time)
        self.track_slider.setValue(self.track_slider.value() + 1000)
        if self.rpc_client.is_connected:
            if self.full_discord_activities:
                self.rpc_client.update(f'{self.current_track_name}', str_time)
            else:
                self.rpc_client.update('Doing something...', random.choice(self.json_data['Emoticons']))
        else:
            self.rpc_client.connectRPC()
            if self.full_discord_activities:
                self.rpc_client.update(f'{self.current_track_name}', str_time)
            else:
                self.rpc_client.update('Doing something...', random.choice(self.json_data['Emoticons']))

def media_status_changed(self):
    # If track is end
    if self.player.mediaStatus() == 7:
        self.track_slider.setValue(0)
        if self.is_repeat:
            pause_or_resume_w_args(self)
        else:
            swith_track(self, 'next')

def player_duration_changed(self):
    set_track_data(self)

def volume_slider_released(self):
    self.player.setVolume(self.volume_slider.value())

def track_slider_released(self):
    self.player.setPosition(self.track_slider.value())
    if not self.track_bigger_than_hour:
        str_time = time.strftime("%M:%S", time.gmtime(
            self.track_slider.value() / 1000))
    else:
        str_time = time.strftime("%H:%M:%S", time.gmtime(
            self.track_slider.value() / 1000))            
    self.current_track_time.setText(str_time)

def playerState(self, state):
    if state == 0:
        self.Play_Pause = False
        self.track_slider.setSliderPosition(1000)

"""
def closeEvent(self, a0: QtGui.QCloseEvent):
    self.hide()
    self.is_waiting_connect = False
    self.player.pause()
    try:
        self.server.close()
    except:
        pass
    self.tray_icon.close()
    with open('extra/json/data.json', 'r', encoding='utf-8') as f:
        self.json_data = json.load(f)
    self.json_data['Rating'] = self.rating
    try:
        self.json_data['Player']['last_track'] = [self.current_track, self.current_track_name]
    except AttributeError:
        self.json_data['Player']['last_track'] = ['', '']
    try:
        self.json_data['Player']['last_playlist'] = self.current_track_playlist
    except AttributeError:
        self.json_data['Player']['last_playlist'] = ''
    try:
        self.json_data['Player']['track_duration'] = self.player.position()
    except AttributeError:
        self.json_data['Player']['track_duration'] = 1
    try:
        self.json_data['Player']['player_slider'] = self.track_slider.sliderPosition()
    except AttributeError:
        self.json_data['Player']['player_slider'] = 1
    try:
        self.json_data['Player']['volume'] = self.volume_slider.value()
    except AttributeError:
        self.json_data['Player']['volume'] = 100
    with open('extra/json/data.json', 'w', encoding='utf-8') as f:
        json.dump(data_without_local_playlist(self),
                    f, indent=4, ensure_ascii=False)
"""