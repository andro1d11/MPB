from PyQt5 import QtCore, QtWidgets, QtMultimedia
from datetime import datetime, timedelta
from init_parsers import init_parsers
import extra.other.func_connections_elements
import extra.other.func_set_change_return_data
import extra.other.func_player_control
import extra.other.func_gui
import extra.other.func_other
import extra.other.func_playlists
import extra.other.parsers
import extra.other.rpc
import socket
import random
import time
import json
import os


def retranslate(self, Form):
    try:
        self.translated_elements = self.lang_data["Translated elements"][self.config["language"]]
        self.sidebar_elements = self.lang_data["Sidebar"][self.config["language"]]
    except KeyError:
        self.translated_elements = self.lang_data["Translated elements"]["English"]
        self.sidebar_elements = self.lang_data["Sidebar"]["English"]
        self.logs_listwidget.addItem('KeyError')
    Form.setWindowTitle("Music PyBox")
    self.current_track_time.setText("0:00")
    self.all_track_time.setText("0:00")
    __sortingEnabled = self.sidebar.isSortingEnabled()
    self.sidebar.setSortingEnabled(False)
    left_sidebar_elements = self.sidebar_elements[0:7]
    for elem in left_sidebar_elements:
        self.sidebar.addItem(elem)
    self.tracks_area.setIconSize(QtCore.QSize(60, 60))
    self.stat_elements = [self.stat_lbl, self.stat_list, self.recomendation_lbl, self.popular_lbl]
    for i in self.rec_list:
        self.stat_elements.append(i)
    for i in self.popular_list:
        self.stat_elements.append(i)
    self.track_area_elements = [self.track_area_action_bttn, self.download_online_data_bttn, self.download_online_data_bttn, self.tracks_area,
                                self.find_track_bttn, self.select_tracks_file_bttn, self.download_playlist_bttn, self.download_with_url_bttn,
                                self.find_track_input]
    self.sidebar.setSortingEnabled(__sortingEnabled)
    self.find_track_bttn.setText(self.translated_elements[10])
    self.select_tracks_file_bttn.setText(self.translated_elements[17])
    self.download_playlist_bttn.setText(self.translated_elements[18])
    self.download_with_url_bttn.setText(self.translated_elements[21])
    self.track_area_action_bttn.setText(self.translated_elements[11])
    self.download_online_data_bttn.setText(self.translated_elements[24])
    self.delete_playlist_bttn.setText(self.translated_elements[5])
    self.next_bttn.setText(">")
    self.prev_bttn.setText("<")
    self.play_bttn.setText("Play")
    self.repeat_bttn.setText(self.translated_elements[19])
    self.settings_bttn.setText(self.translated_elements[20])
    self.volume_lbl.setText(self.translated_elements[16])
    self.queue_lbl.setText(self.translated_elements[15])
    self.logs_lbl.setText('Logs')
    self.stat_lbl.setText(self.translated_elements[8])
    self.recomendation_lbl.setText(self.translated_elements[22])
    self.popular_lbl.setText(self.translated_elements[23])

    # Init qmediaplayer
    self.player = QtMultimedia.QMediaPlayer()

    # Connectin gui elements
    self.play_bttn.clicked.connect(
        lambda: extra.other.func_player_control.pause_or_resume(self))
    self.find_track_bttn.clicked.connect(
        lambda: extra.other.func_other.find_tracks_to_lyrics(self))
    self.select_tracks_file_bttn.clicked.connect(
        lambda: extra.other.func_set_change_return_data.open_tracks_file_Dialog(self))
    self.download_playlist_bttn.clicked.connect(
        lambda: extra.other.func_other.download_playlist(self))
    self.download_with_url_bttn.clicked.connect(
        lambda: extra.other.func_other.parse_track_only_url(self))
    self.track_area_action_bttn.clicked.connect(
        lambda: extra.other.func_set_change_return_data.select_action(self))
    self.find_track_input.textChanged.connect(
        lambda: extra.other.func_set_change_return_data.search_for_playlist(self))
    self.download_online_data_bttn.clicked.connect(
        lambda: extra.other.func_other.save_for_online(self))
    self.rate_result_bttn.clicked.connect(
        lambda: extra.other.func_set_change_return_data.rate_track(self))
    self.playlists.clicked.connect(
        lambda: extra.other.func_gui.load_playlist(self))
    self.playlists.itemDoubleClicked.connect(
        lambda: extra.other.func_playlists.add_track_to_playlist(self))
    self.delete_playlist_bttn.clicked.connect(
        lambda: extra.other.func_playlists.delete_playlist(self))
    self.tracks_area.itemDoubleClicked.connect(
        lambda: extra.other.func_gui.select_track(self))
    self.tracks_area.itemSelectionChanged.connect(
        lambda: extra.other.func_set_change_return_data.set_temp_tracks(self))
    self.tracks_area.model().rowsMoved.connect(
        lambda: extra.other.func_set_change_return_data.update_json_data(self))
    self.sidebar.clicked.connect(
        lambda: extra.other.func_gui.left_sidebar_action(self))
    self.next_bttn.clicked.connect(
        lambda: extra.other.func_player_control.swith_track(self, 'next'))
    self.prev_bttn.clicked.connect(
        lambda: extra.other.func_player_control.swith_track(self, 'prev'))
    self.repeat_bttn.clicked.connect(
        lambda: extra.other.func_player_control.change_repeat(self))
    self.settings_bttn.clicked.connect(
        lambda: extra.other.func_other.open_settings(self))
    self.player.mediaStatusChanged.connect(
        lambda: extra.other.func_connections_elements.media_status_changed(self))
    self.player.durationChanged.connect(
        lambda: extra.other.func_connections_elements.player_duration_changed(self))
    self.player.stateChanged.connect(
        lambda: extra.other.func_connections_elements.playerState)
    self.track_slider.sliderMoved.connect(
        lambda: extra.other.func_connections_elements.track_slider_released(self))
    self.volume_slider.valueChanged.connect(
        lambda: extra.other.func_connections_elements.volume_slider_released(self))
    extra.other.func_gui.hide_elements(
        self.stat_elements)
    extra.other.func_gui.hide_elements(
        self.rate_elems)
    extra.other.func_gui.hide_elements([self.tracks_area, self.find_track_input, self.find_track_bttn, self.download_online_data_bttn,
                        self.select_tracks_file_bttn, self.download_playlist_bttn, self.download_with_url_bttn, self.track_area_action_bttn,])

    # Vars
    with open('extra/json/temp.json', 'r', encoding='utf-8') as f:
        self.urls = json.load(f)['search_result']
    with open('extra/json/data.json', 'r', encoding='utf-8') as f:
        self.json_data = json.load(f)
    with open('extra/json/config.json', 'r') as f:
        self.config = json.load(f)
        self.client_id = self.config['rpc_client_id']
        self.debug_mode = self.config['debug']
        self.ofline_mode = self.config['ofline']
        
    self.current_track = ''
    self.selected_playlist = ''
    self.action = 'playlist'
    self.tracks_to_lyrics = {}
    self.online_tracks_data = {}
    self.queue = []
    self.temp_tracks = []
    self.rate_result = 4
    self.Play_Pause = True
    self.first_play = True
    self.is_downloading_now = False
    self.is_repeat = False
    self.its_online_track = False
    self.track_bigger_than_hour = False
    need_update_recomendations = False
    try:
        self.current_track = self.json_data['Player']['last_track'][0]
        self.current_track_name = self.json_data['Player']['last_track'][1]
        self.current_track_playlist = self.json_data['Player']['last_playlist']
        self.rating = self.json_data['Rating']
    except:
        pass
    if self.corrupted_data:
        self.logs_listwidget.addItem('Data was corrupted. Backup loaded.')
    self.next_week = (datetime.now() + timedelta(7)).strftime('%d.%m.%y')
    self.next_day = (datetime.now() + timedelta(1)).strftime('%d.%m.%y')

    # Net elements
    parsers = init_parsers(debug=self.debug_mode)
    parsers.start_threads()
    self.parser_lyrics, self.parser_youtube, self.parser_lastfm = parsers.result

    if not self.ofline_mode:
        if False in [self.parser_youtube.connection, self.parser_lyrics.connection, self.parser_lastfm.connection]:
            self.net_mode = 1
            try:
                self.parser_lastfm.quit_webdriver()
            except:
                pass
        else:
            self.net_mode = 0
    else:
        self.net_mode = 1
        try:
            self.parser_lastfm.quit_webdriver()
        except:
            pass
    self.rpc_client = extra.other.rpc.rpc(self.client_id, self)
    self.rpc_client.update('Doing something...', random.choice(self.json_data['Emoticons']))

    # Threads
    if self.net_mode == 0:
        self.parse_tracks_thread = extra.other.parsers.parse_tracks_urls_thread(
            mainWindow=self)
        self.download_track_thread = extra.other.parsers.download_track_thread(mainWindow=self)
        self.download_playlist_thread = extra.other.parsers.download_playlist_thread(
            mainWindow=self)
        self.get_tracks_to_lyrics_thread = extra.other.parsers.get_tracks_to_lyrics_thread(
            mainWindow=self)
        self.get_lyrics_thread = extra.other.parsers.get_lyrics_thread(mainWindow=self)

    # Setting next week date for clearing statistic
    if self.json_data['Date']['next_week_date'] == '0':
        with open('extra/json/data.json', 'w') as f:
            self.json_data['Date']['next_week_date'] = self.next_week
            f.write(self.next_week)
    else:
        try:
            self.old_next_week = datetime.strptime(self.json_data['Date']['next_week_date'], '%d.%m.%y')
        except ValueError:
            self.old_next_week = datetime.now()
        if self.old_next_week < datetime.now():
            with open('extra/json/data.json', 'w', encoding='utf-8') as f:
                self.json_data['Statistic']['amount_plays'] = {}
                self.json_data['Date']['next_week_date'] = self.next_week
                json.dump(self.json_data, f, ensure_ascii=False, indent=4)

    # Setting next day date for setting new recomendations every day
    if self.json_data['Date']['next_day_date'] == '0':
        with open('extra/json/data.json', 'w') as f:
            self.json_data['Date']['next_day_date'] = self.next_day
            f.write(self.next_day)
        need_update_recomendations = True
    else:
        try:
            self.old_next_day = datetime.strptime(self.json_data['Date']['next_day_date'], '%d.%m.%y')
        except ValueError:
            self.old_next_day = datetime.now()
        if self.old_next_day <= datetime.now():
            with open('extra/json/data.json', 'w', encoding='utf-8') as f:
                self.json_data['Date']['next_day_date'] = self.next_day
                json.dump(self.json_data, f, ensure_ascii=False, indent=4)
            need_update_recomendations = True

    # Setting recomendations to main page 
    if self.net_mode == 0:
        if len(os.listdir('extra/imgs_recomended')) != 4 or need_update_recomendations:
            print('Recomendation update')
            popular_tracks_temp = {}
            unsorted_popular_tracks_temp = self.json_data['Statistic']['amount_plays']
            sorted_popular_tracks_temp_keys = sorted(
                unsorted_popular_tracks_temp, key=unsorted_popular_tracks_temp.get, reverse=True)
            for w in sorted_popular_tracks_temp_keys:
                popular_tracks_temp[w] = unsorted_popular_tracks_temp[w]
            for i in os.listdir('extra/imgs_recomended'):
                os.remove(f'extra/imgs_recomended/{i}')
            i = 0
            for track in list(popular_tracks_temp.keys()):
                if self.parser_lastfm.get_track(track):
                    i += 1
                    if i == 4:
                        break
                else:
                    continue
        self.parser_lastfm.quit_webdriver()
    i = 0
    for file in os.listdir('extra/imgs_recomended'):
        self.rec_list[i].update(
            file[:-4], os.path.abspath(f'extra/imgs_recomended/{file}'))
        i += 1

    # Setting popular tracks to main page
    popular_tracks_temp = {}
    unsorted_popular_tracks_temp = self.json_data['Statistic']['amount_plays']
    sorted_popular_tracks_temp_keys = sorted(
        unsorted_popular_tracks_temp, key=unsorted_popular_tracks_temp.get, reverse=True)
    for w in sorted_popular_tracks_temp_keys:
        popular_tracks_temp[w] = unsorted_popular_tracks_temp[w]

    i = 0
    for cell in self.popular_list:
        try:
            track_name = list(popular_tracks_temp.keys())[i]
            cell.update(extra.other.func_set_change_return_data.redact_text(self, track_name, 30), os.path.abspath(f'extra/files/{str(sorted_popular_tracks_temp_keys[i])}.jpg'))
        except IndexError:
            pass
        i += 1

    # Get local ip
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        self.host_name = sock.getsockname()[0]
        sock.close()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host_name, 7777))
    except Exception as exc:
        self.logs_listwidget.addItem(str(exc))

    # Track file exist?
    if not os.path.exists(self.current_track):
        self.current_track = ''
        self.current_track_name = ''
        self.current_track_playlist = ''

    # Set some text
    if self.net_mode == 1:
        parsers_status = f'YouTube:{self.parser_youtube.connection}\nLyrics:{self.parser_youtube.connection}\nLastFm:{self.parser_lastfm.connection}'
        self.logs_listwidget.addItem('OFFLINE MODE ENABLE')
        self.logs_listwidget.addItem(parsers_status)
    self.track_name_lbl.setText(self.current_track_name)
    self.playlists_data = os.listdir('files')

    for track in self.playlists_data:
        item = QtWidgets.QListWidgetItem('files/' + track)
        self.tracks_area.addItem(item)
        self.json_data['Playlists']['Local'].append('files/' + track)
        if track.split('.mp3')[-1] == '':
            if track.replace('.mp3', '') not in self.json_data['Statistic']['amount_plays']:
                self.json_data['Statistic']['amount_plays'][track.replace('.mp3', '')] = 0

    try:
        self.current_track_item = self.tracks_area.findItems(
            self.current_track_name, QtCore.Qt.MatchExactly)[0]
    except:
        self.current_track_item = None
    with open('extra/json/data.json', 'w', encoding='utf-8') as f:
        json.dump(extra.other.func_set_change_return_data.data_without_local_playlist(self),
                    f, ensure_ascii=False, indent=4)
    self.json_playlists = list(self.json_data['Playlists'])
    for playlist in self.json_playlists:
        self.playlists.addItem(playlist)

    try:
        self.player.setVolume(self.json_data['Player']['volume'])
        self.volume_slider.setValue(self.json_data['Player']['volume'])
        self.track_time_data = extra.other.func_set_change_return_data.return_human_time_from_track_pyglet(self, self.current_track)
        self.track_time = self.track_time_data[0]
        self.all_track_time.setText(self.track_time_data[1])

        # Load player data from data file
        self.track_slider.setMinimum(0)
        self.track_slider.setMaximum(int(self.track_time))
        self.track_slider.setValue(
            self.json_data['Player']['track_duration'])
        self.player.setMedia(QtMultimedia.QMediaContent(
            QtCore.QUrl(self.current_track)))
        self.player.setPosition(self.track_slider.value())
        if self.json_data['Player']['track_duration'] >= 3600000:
            self.current_track_time.setText(time.strftime(
                "%H:%M:%S", time.gmtime(self.json_data['Player']['track_duration'] / 1000)))
        else:
            self.current_track_time.setText(time.strftime(
                "%M:%S", time.gmtime(self.json_data['Player']['track_duration'] / 1000)))
        extra.other.func_connections_elements.track_slider_released(self)

    except Exception as exc:
        self.logs_listwidget.addItem('Load data error')
        self.logs_listwidget.addItem(str(exc))
        