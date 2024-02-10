from PyQt5 import QtCore, QtWidgets, QtGui
from extra.other.custom_widgets import *
import extra.other.func_set_change_return_data
import extra.other.func_playlists
import extra.other.func_other
import win32com.client as com
import threading
import random
import json
import os


def left_sidebar_action(self):
    current_sidebar_index = self.sidebar.indexFromItem(
        self.sidebar.currentItem()).row()
    # Main
    if current_sidebar_index == 0:
        self.is_waiting_connect = False
        hide_elements(self.track_area_elements)
        hide_elements(self.rate_elems)
        show_elements(self.stat_elements)
        self.stat_list.clear()

        fso = com.Dispatch("Scripting.FileSystemObject")
        folder = fso.GetFolder('files')
        mb = 1024 * 1024.0
        files_folder_size = "{}".format(round(folder.Size/mb, 1))
        self.stat_list.addItem(
            f'Розмір папки /files: \t{files_folder_size} мб')

    # Search
    elif current_sidebar_index == 1:
        if self.net_mode == 1:
            self.logs_listwidget.addItem('OFFLINE MODE ENABLE')
        else:
            self.is_waiting_connect = False
            hide_elements(self.stat_elements)
            hide_elements(self.rate_elems)
            with open('extra/json/temp.json', 'r', encoding='utf-8') as f:
                temp_data = json.load(f)
                self.urls = temp_data['search_result']
                self.find_track_input.setText(temp_data['input_data'])
            self.tracks_area.setStyleSheet(self.tracks_area_stylesheets)
            self.tracks_area.clear()
            if self.urls != False:
                for i in self.urls:
                    self.tracks_area.addItem(i)
            self.action = 'download'
            show_elements([self.tracks_area, self.find_track_input, self.find_track_bttn, self.download_online_data_bttn,
                                self.select_tracks_file_bttn, self.download_playlist_bttn, self.download_with_url_bttn, self.track_area_action_bttn])
            self.track_area_action_bttn.setText(
                self.translated_elements[11])

    # Lyrics
    elif current_sidebar_index == 2:
        if self.net_mode == 1:
            self.logs_listwidget.addItem('OFFLINE MODE ENABLE')
        else:
            self.is_waiting_connect = False
            hide_elements(self.stat_elements)
            hide_elements(self.rate_elems)
            hide_elements([self.select_tracks_file_bttn, self.track_area_action_bttn,
                                self.download_online_data_bttn, self.download_with_url_bttn,
                                self.download_playlist_bttn])
            show_elements(
                [self.find_track_input, self.find_track_bttn, self.tracks_area])
            self.find_track_input.setText(self.current_track_name)
            self.tracks_area.setStyleSheet(self.tracks_area_stylesheets)
            self.tracks_area.clear()
            self.track_to_lyrics_temp = self.current_track_name
            self.action = 'lyrics'
            if self.current_track != '':
                if self.current_track_playlist == 'local' or self.track_to_lyrics_temp.split('files/')[0] == '' and self.track_to_lyrics_temp.split('files/')[1].split('.mp3')[-1] == '':
                    self.find_track_input.setText(
                        self.return_clear_track_name(self.current_track_name))
                    self.track_to_lyrics_temp = self.return_clear_track_name(
                        self.track_to_lyrics_temp)
            with open('extra/json/temp.json', 'r', encoding='utf-8') as f:
                temp_data = json.load(f)
            for i in temp_data['lyrics_data']['lyrics']:
                self.tracks_area.addItem(i)

    # Rate
    elif current_sidebar_index == 3:
        self.rate_track_name_lbl.setText(self.current_track_name)
        hide_elements(self.stat_elements)
        hide_elements([self.tracks_area, self.find_track_input, self.find_track_bttn, self.download_online_data_bttn,
                        self.select_tracks_file_bttn, self.download_playlist_bttn, self.download_with_url_bttn, self.track_area_action_bttn,])
        show_elements(self.rate_elems)

    # Rating
    elif current_sidebar_index == 4:
        hide_elements(self.stat_elements)
        hide_elements(self.rate_elems)
        hide_elements([self.tracks_area, self.find_track_input, self.find_track_bttn, self.download_online_data_bttn,
                        self.select_tracks_file_bttn, self.download_playlist_bttn, self.download_with_url_bttn, self.track_area_action_bttn,])
        show_elements([self.tracks_area])
        stylesheet = '\\QWidget#tracks_area{font: 30px; background-color: #121212;}\\QWidget#tracks_area::item{border: 5px solid #121212; border-radius: 5px; background-color: #121212;}\\QWidget#tracks_area::item:hover{background-color: #786262; color: #FFFFFF}\\QWidget#tracks_area::item:selected{background-color: #786262; color: #FFFFFF}'
        self.tracks_area.setStyleSheet(stylesheet)
        self.tracks_area.clear()
        self.action = 'rating'
        self.kom = dict(sorted(self.rating.items(), key=lambda item: item[1], reverse=True))
        for track in self.kom.keys():
            widget = RatingCell(self, track, 'test', self.rating[track])
            icon_path = f'extra/files/{track}.jpg'
            if not os.path.exists(icon_path):
                icon_path = 'extra/imgs/default_pic.jpg'
            icon = QtGui.QIcon(icon_path)
            item = QtWidgets.QListWidgetItem(icon, '')
            self.tracks_area.insertItem(self.tracks_area.count(), item)
            self.tracks_area.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    # New playlist
    elif current_sidebar_index == 5:
        self.is_waiting_connect = False
        if self.find_track_input.isHidden():
            hide_elements([self.track_area_action_bttn])
            hide_elements(self.stat_elements)
            hide_elements(self.rate_elems)
            show_elements([self.find_track_input, self.tracks_area])
            self.tracks_area.clear()
            self.track_area_action_bttn.setText(
                self.translated_elements[12])
        else:
            extra.other.func_playlists.create_playlist(self)

    # Connect to device
    elif current_sidebar_index == 6:
        self.action = 'connect'
        self.tracks_area.setStyleSheet(self.tracks_area_stylesheets)
        self.tracks_area.clear()
        if self.tracks_area.isHidden():
            self.tracks_area.show()
            hide_elements(self.stat_elements)
            hide_elements(self.rate_elems)
            hide_elements([self.find_track_input, self.find_track_bttn, self.download_online_data_bttn,
                                self.download_playlist_bttn, self.download_with_url_bttn, self.download_online_data_bttn])
        self.secret_code = random.randint(1000, 9999)
        self.track_area_action_bttn.setText(self.translated_elements[13])
        self.tracks_area.addItem(self.translated_elements[14])
        self.tracks_area.addItem(f'IP:\t{self.host_name}')
        self.tracks_area.addItem(f'PORT:\t{7777}')
        self.tracks_area.addItem(f'CODE:\t{self.secret_code}')

        self.is_waiting_connect = True
        at = threading.Thread(target=lambda: extra.other.func_other.accept_connection)
        at.start()

def select_track(self):
    try:
        if self.action == 'playlist':
            if self.selected_playlist == 'Local':
                if self.current_track_name != self.tracks_area.currentItem().text() and self.current_track != self.tracks_area.currentItem().text():
                    self.track_slider.setValue(0)
                    self.current_track_name = self.tracks_area.currentItem().text()
                    self.current_track = self.tracks_area.currentItem().text()
                    self.current_track_playlsit_obj = self.playlists.currentItem()
                    self.current_track_playlist = self.playlists.currentItem().text()
                    extra.other.func_set_change_return_data.pause_or_resume_w_args(self)
            else:
                with open('extra/json/data.json', 'r', encoding='utf-8') as f:
                    self.json_data = json.load(f)

                if self.current_track_name != self.tracks_area.currentItem().text() and self.current_track != self.json_data['Playlists'][self.selected_playlist][self.tracks_area.currentItem().text()]:
                    self.track_slider.setValue(0)
                    self.current_track_name = self.tracks_area.currentItem().text()
                    self.current_track = self.json_data['Playlists'][self.selected_playlist][self.tracks_area.currentItem().text()]

                    if self.current_track.split(' ')[0] == 'ONLINE_TRACK':
                        if self.net_mode != 1:
                            if self.current_track_name in list(self.online_tracks_data.keys()):
                                best_audio = self.current_track_name
                            else:
                                best_audio = self.parser_youtube.get_best_audio(self.current_track.split(' ')[1])
                            self.its_online_track = True
                            self.current_track = best_audio
                    else:
                        self.its_online_track = False

                    self.current_track_playlist = self.playlists.currentItem().text()
                    extra.other.func_set_change_return_data.pause_or_resume_w_args(self)

        elif self.action == 'lyrics':
            self.get_lyrics_thread.start()
    except KeyError:
        pass

def load_playlist(self):
    if self.action != 'playlist':
        self.find_track_input.clear()
    self.temp_playlist = self.selected_playlist
    self.selected_playlist = self.playlists.currentItem().text()
    self.track_area_action_bttn.setText(self.translated_elements[12])
    self.action = 'playlist'
    self.old_temp_tracks = []
    hide_elements(self.stat_elements)
    hide_elements(self.rate_elems)
    hide_elements([self.find_track_bttn, self.download_online_data_bttn,
                        self.download_playlist_bttn, self.download_with_url_bttn, self.select_tracks_file_bttn])
    show_elements([self.track_area_action_bttn, self.tracks_area, self.find_track_input])
    self.tracks_area.setStyleSheet(self.tracks_area_stylesheets)
    self.tracks_area.clear()

    for i in self.temp_tracks:
        self.old_temp_tracks.append(i)

    if self.selected_playlist == 'Local':
        temp_header_item = QtWidgets.QListWidgetItem()
        playlist_header = PlaylistHeader()
        self.tracks_area.insertItem(self.tracks_area.count(), temp_header_item)
        self.tracks_area.setItemWidget(temp_header_item, playlist_header)
        temp_header_item.setSizeHint(QtCore.QSize(578, 229))
    
        self.playlists_data = os.listdir('files')
        with open('extra/json/data.json', 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
        pixmap_matrix = []
        for track in self.playlists_data:
            if track.split('.mp3')[-1] == '':
                icon_path = 'extra/files/' + track[:-4] + '.jpg'
                if os.path.exists(icon_path):
                    icon_path = icon_path
                else:
                    icon_path = 'extra/imgs/default_pic.jpg'
                    
                icon = QtGui.QIcon(icon_path)
                pixmap_matrix.append(icon_path)
                item = QtWidgets.QListWidgetItem(icon, 'files/' + track)
                self.tracks_area.addItem(item)

                self.json_data['Playlists']['Local'].append('files/' + track)
        playlist_header.update(pixmap_matrix, self.selected_playlist, len(self.playlists_data))

    else:
        temp_header_item = QtWidgets.QListWidgetItem()
        playlist_header = PlaylistHeader()
        self.tracks_area.insertItem(0, temp_header_item)
        temp_header_item.setSizeHint(QtCore.QSize(578, 229))

        with open('extra/json/data.json', 'r', encoding='utf-8') as f:
            self.playlists_data = json.load(f)
        pixmap_matrix = []
        for track in self.playlists_data['Playlists'][self.selected_playlist]:
            if track.split('files/')[0] == '':
                icon_path = 'extra/files/' + track.split('files/')[1][:-4] + '.jpg'
                if os.path.exists(icon_path):
                    pixmap_matrix.append(icon_path)
                else:
                    icon_path = 'extra/imgs/default_pic.jpg'
                    pixmap_matrix.append(icon_path)
            else:
                icon_path = 'extra/files/' + track + '.jpg'
                if os.path.exists(icon_path):
                    pixmap_matrix.append(icon_path)
                else:
                    icon_path = 'extra/imgs/default_pic.jpg'
                    pixmap_matrix.append(icon_path)
            self.tracks_area.addItem(QtWidgets.QListWidgetItem(QtGui.QIcon(icon_path), track))
        playlist_header.update(pixmap_matrix, self.selected_playlist, len(self.playlists_data['Playlists'][self.selected_playlist]))

        self.tracks_area.setItemWidget(temp_header_item, playlist_header)
    try:
        self.current_track_item = self.tracks_area.findItems(
            self.current_track_name, QtCore.Qt.MatchExactly)[0]
        scroll_to_elem(self)
    except IndexError:
        pass

def select_element(self):
    if self.action == 'playlist':
        try:
            self.current_track_item.setSelected(False)
        except:
            pass
        self.current_track_item = self.tracks_area.findItems(
            self.current_track_name, QtCore.Qt.MatchExactly)[0]
        for i in self.temp_tracks:
            try:
                self.tracks_area.findItems(i, QtCore.Qt.MatchExactly)[0]
            except IndexError:
                pass
        self.current_track_item.setSelected(True)

def scroll_to_elem(self):
    try:
        select_element(self)
        self.tracks_area.scrollToItem(
            self.current_track_item, QtWidgets.QAbstractItemView.PositionAtCenter)
    except Exception as exc:
        self.logs_listwidget.addItem(str(exc))

def hide_elements(elems):
    for i in elems:
        i.hide()

def show_elements(elems):
    for i in elems:
        i.show()