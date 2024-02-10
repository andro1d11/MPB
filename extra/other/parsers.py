from PyQt5.QtCore import QThread, QObject
import extra.other.func_playlists
import extra.other.setup_ui
import threading
import json
import time


class get_tracks_to_lyrics_thread(QThread):
    def __init__(self, mainWindow, parent=None):
        QObject.__init__(self, parent=parent)
        self.mainWindow = mainWindow
        self.stop_search = 0
        self.mainWindow.tracks_area.clear()
        with open('extra/json/config.json', 'r') as f:
            self.config = json.load(f)

    def run(self):
        try:
            if self.mainWindow.action == 'lyrics':
                self.mainWindow.tracks_area.clear()
                self.mainWindow.tracks_area.addItem('Wait...')
            self.mainWindow.tracks_to_lyrics = self.mainWindow.parser_lyrics.get_tracks(
                self.mainWindow.track_to_lyrics_temp)
            if self.mainWindow.action == 'lyrics':
                self.mainWindow.tracks_area.clear()
            self.stop_search += 1
            if self.mainWindow.sidebar.indexFromItem(self.mainWindow.sidebar.currentItem()).row() == 2:
                # If the lyrics are not received 5 times
                if self.stop_search >= 5:
                    if self.mainWindow.action != 'playlist':
                        if self.mainWindow.action == 'lyrics':
                            self.mainWindow.tracks_area.addItem(
                                'Lyrics for track not found! :(')
                            self.mainWindow.find_track_bttn.show()
                    self.stop_search = 0
                # Else rerun
                else:

                    if len(list(self.mainWindow.tracks_to_lyrics)) == 0:
                        self.run()
                    # If lyrics found
                    else:
                        if self.mainWindow.action == 'lyrics':
                            for i in list(self.mainWindow.tracks_to_lyrics.keys()):
                                self.mainWindow.tracks_area.addItem(i + '\n')
                            self.mainWindow.action = 'lyrics'
                            self.mainWindow.find_track_bttn.show()
                        self.stop_search = 0
            else:
                self.stop_search = 0
        except Exception as exc:
            self.mainWindow.logs_listwidget.addItem(str(exc))


class get_lyrics_thread(QThread):
    def __init__(self, mainWindow, parent=None):
        QObject.__init__(self, parent=parent)
        self.mainWindow = mainWindow
        with open('extra/json/config.json', 'r') as f:
            self.config = json.load(f)
        with open('extra/json/lang.json', 'r', encoding='utf-8') as f:
            self.lang_data = json.load(f)
        try:
            self.translated_elements = self.lang_data["Translated elements"][self.config["language"]]
        except KeyError:
            self.translated_elements = self.lang_data["Translated elements"]["English"]

    def run(self):
        lyrics_track = self.mainWindow.tracks_area.currentItem().text().replace('\n', '')
        try:
            lyrics = self.mainWindow.parser_lyrics.get_lyrics(
                self.mainWindow.tracks_to_lyrics[lyrics_track].replace('\n', ''))
            lyrics = lyrics.split('\n')
            if self.mainWindow.action == 'lyrics':
                self.mainWindow.tracks_area.clear()
                for i in lyrics:
                    self.mainWindow.tracks_area.addItem(i)
            # Adding lyrics to temp
            with open('extra/json/temp.json', 'r', encoding='utf-8') as f:
                temp_data = json.load(f)
            temp_data['lyrics_data']['lyrics_track'] = self.mainWindow.track_to_lyrics_temp
            temp_data['lyrics_data']['lyrics'] = lyrics
            lyrics = ''
            with open('extra/json/temp.json', 'w', encoding='utf-8') as f:
                json.dump(temp_data, f, ensure_ascii=False, indent=4)
            temp_data = ''
            del self.mainWindow.tracks_to_lyrics, lyrics
        except:
            pass


class parse_tracks_urls_thread(QThread):
    def __init__(self, mainWindow, parent=None):
        QObject.__init__(self, parent=parent)
        self.mainWindow = mainWindow
        with open('extra/json/config.json', 'r') as f:
            self.config = json.load(f)
        with open('extra/json/lang.json', 'r', encoding='utf-8') as f:
            self.lang_data = json.load(f)
        try:
            self.translated_elements = self.lang_data["Translated elements"][self.config["language"]]
        except KeyError:
            self.translated_elements = self.lang_data["Translated elements"]["English"]

    def run(self):
        self.mainWindow.find_track_bttn.hide()
        self.mainWindow.tracks_area.clear()
        self.mainWindow.tracks_area.addItem('Wait...')
        track_name = self.mainWindow.find_track_input.text()
        self.mainWindow.urls = self.mainWindow.parser_youtube.get_urls(track_name)
        # Add to temp
        with open('extra/json/temp.json', 'r', encoding='utf-8') as f:
            temp_data = json.load(f)
        temp_data['search_result'] = self.mainWindow.urls
        temp_data['input_data'] = track_name
        with open('extra/json/temp.json', 'w', encoding='utf-8') as f:
            json.dump(temp_data, f, indent=4, ensure_ascii=False)

        # If urls found
        if self.mainWindow.urls != False:
            self.mainWindow.tracks_area.clear()
            for url in self.mainWindow.urls:
                self.mainWindow.tracks_area.addItem(url)
            if len(self.mainWindow.tracks_area) != 0:
                self.mainWindow.track_area_action_bttn.show()
            self.mainWindow.find_track_bttn.show()


class download_track_thread(QThread):
    def __init__(self, mainWindow, parent=None):
        QObject.__init__(self, parent=parent)
        self.mainWindow = mainWindow
        with open('extra/json/config.json', 'r') as f:
            self.config = json.load(f)
        with open('extra/json/lang.json', 'r', encoding='utf-8') as f:
            self.lang_data = json.load(f)
        try:
            self.translated_elements = self.lang_data["Translated elements"][self.config["language"]]
        except KeyError:
            self.translated_elements = self.lang_data["Translated elements"]["English"]

    def download_asynchronously(self, url, img_url, path, song_name):
        # Get track title if you search track with url
        if song_name == 'Track from URL':
            song_name = self.mainWindow.parser_youtube.get_title(url)

        dt = threading.Thread(target=lambda: self.mainWindow.parser_youtube.download_track(
            url, img_url, path, song_name))
        try:
            dt.start()
            while True:
                if not dt.is_alive():
                    for i in range(self.mainWindow.queue_listwidget.count()):
                        if self.mainWindow.queue_listwidget.item(i).text() == song_name:
                            self.mainWindow.queue_listwidget.takeItem(i)
                            extra.other.func_playlists.add_track_to_json(self, 'Downloads', song_name, f'files/{song_name}.mp3')
                            break
                    if self.mainWindow.queue_list_widget.count() == 0:
                        self.mainWindow.parser_youtube.rename_files('files')
                    break

        except Exception as exc:
            print(exc)
            for i in range(self.mainWindow.queue_listwidget.count()):
                if self.mainWindow.queue_listwidget.item(i).text() == song_name:
                    self.mainWindow.queue_listwidget.takeItem(i)

    def run(self):
        for i in self.mainWindow.queue:
            self.mainWindow.is_downloading_now = True
            song_name = i['song_name']
            url = i['url']
            img_url = i['img_url']
            if song_name != None:
                song_name = song_name.replace('?', '')

            DaT = threading.Thread(target=lambda: self.download_asynchronously(
                url, img_url, 'files', song_name))
            DaT.start()

            # Add to statistic
            with open('extra/json/data.json', 'r', encoding='utf-8') as f:
                self.mainWindow.json_data = json.load(f)
            if song_name in self.mainWindow.json_data['Statistic']['amount_plays']:
                pass
            else:
                self.mainWindow.json_data['Statistic']['amount_plays'][song_name] = 0
            with open('extra/json/data.json', 'w', encoding='utf-8') as f:
                json.dump(self.mainWindow.json_data, f,
                          indent=4, ensure_ascii=False)

            self.mainWindow.track_area_action_bttn.setText(
                self.translated_elements[11])
            self.mainWindow.queue.remove(i)
        self.mainWindow.is_downloading_now = False


class download_tracks_from_file_thread(QThread):
    def __init__(self, mainWindow, tracks, parent=None):
        QObject.__init__(self, parent=parent)
        self.mainWindow = mainWindow
        self.tracks = tracks

    def run(self):
        try:
            for track in self.tracks:
                founded_tracks = self.mainWindow.parser_youtube.get_urls(track)
                first_track = {list(founded_tracks.keys())[
                    0]: list(founded_tracks.values())[0]}

                song_name = list(first_track.keys())[0]
                url = first_track[song_name][0]
                img_url = first_track[song_name][1]

                self.mainWindow.queue_listwidget.addItem(song_name)
                self.mainWindow.queue.append(
                    {'song_name': song_name, 'url': url, 'img_url': img_url})
            self.mainWindow.download_track_thread.start()
        except Exception as exc:
            self.mainWindow.logs_listwidget.addItem(str(exc))


class download_playlist_thread(QThread):
    def __init__(self, mainWindow, parent=None):
        QObject.__init__(self, parent=parent)
        self.mainWindow = mainWindow

    def run(self):
        self.playlist_url = self.mainWindow.find_track_input.text()
        time.sleep(0.5)
        playlist = self.mainWindow.parser_youtube.get_playlist(self.playlist_url)
        if playlist == False:
            self.mainWindow.logs_listwidget.addItem('Parser Error. Try again')
        else:
            for track in playlist.keys():
                song_name = track
                url = playlist[track][0]
                img_url = playlist[track][1]

                self.mainWindow.queue_listwidget.addItem(song_name)
                self.mainWindow.queue.append(
                    {'song_name': song_name, 'url': url, 'img_url': img_url})
            self.mainWindow.download_track_thread.start()


if __name__ == '__main__':
    pass