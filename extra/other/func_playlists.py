import extra.other.func_set_change_return_data
import extra.other.func_gui
import json
import os


def add_track_to_playlist(self):
    try:
        self.playlist_to_add = self.playlists.currentItem().text()
        if self.playlist_to_add != 'Local':
            if self.temp_playlist != 'Local':
                for temp_track in self.old_temp_tracks:
                    self.json_data['Playlists'][self.playlist_to_add][
                        temp_track] = self.json_data['Playlists'][self.temp_playlist][temp_track]
            elif self.temp_playlist == 'Local':
                for temp_track in self.temp_tracks:
                    self.json_data['Playlists'][self.playlist_to_add][temp_track] = temp_track
        with open('extra/json/data.json', 'w', encoding='utf-8') as f:
            json.dump(extra.other.func_set_change_return_data.data_without_local_playlist(self),
                        f, indent=4, ensure_ascii=False)
        extra.other.func_gui.load_playlist(self)
    except KeyError:
        self.logs_listwidget.addItem('KeyError')

def delete_track_form_playlist(self):
    self.prev_current_track = self.current_track
    self.deleted_elements = self.tracks_area.selectedItems()
    current_playlist = self.playlists.currentItem().text()
    try:
        self.deleted_elements_text = []
        for i in self.tracks_area.selectedItems():
            self.deleted_elements_text.append(i.text())
    except AttributeError:
        self.logs_listwidget.addItem('AttributeError')
        return 0

    if current_playlist == 'Local':
        for i in extra.other.func_set_change_return_data.find_track_in_playlists(self, self.deleted_elements_text):
            for j in self.deleted_elements_text:
                self.json_data['Playlists'][i] = {
                    key: val for key, val in self.json_data['Playlists'][i].items() if val != j}
        self.json_data['Playlists']['Local'] = []
        # Adding all tracks from /files to json data
        for i in os.listdir('files'):
            self.json_data['Playlists']['Local'].append('files/' + i)
        # Removing file
        try:
            for i in self.deleted_elements_text:
                pass
                os.remove(self.json_data['Playlists']['Local']
                            [self.json_data['Playlists']['Local'].index(i)])
                os.remove('extra/' + self.json_data['Playlists'][current_playlist][self.json_data['Playlists']
                            [current_playlist].index(i)][:-4] + '.jpg')  # self.deleted_element_text
        except FileNotFoundError:
            self.logs_listwidget.addItem('FileNotFoundError')

    for r in range(len(self.deleted_elements_text)):
        try:
            k = self.deleted_elements[r]
            i = self.deleted_elements_text[r]
            if type(self.json_data['Playlists'][current_playlist]) == dict:
                json_data_playlist_keys = list(
                    self.json_data['Playlists'][current_playlist].keys())
                json_data_playlist_values = list(
                    self.json_data['Playlists'][current_playlist].values())

                if i == self.current_track_name:
                    for j in range(len(json_data_playlist_values)):
                        if json_data_playlist_values[j] == self.json_data['Playlists'][current_playlist][i]:
                            if j == len(json_data_playlist_values) - 1:
                                find_next_track = json_data_playlist_keys[j - 1]
                                self.current_track = self.json_data['Playlists'][current_playlist][find_next_track]
                                self.current_track_name = find_next_track
                                extra.other.func_set_change_return_data.pause_or_resume_w_args(self)
                                extra.other.func_gui.select_element(self)
                                break
                            else:
                                find_next_track = json_data_playlist_keys[j + 1]
                                self.current_track = self.json_data['Playlists'][current_playlist][find_next_track]
                                self.current_track_name = find_next_track
                                extra.other.func_set_change_return_data.pause_or_resume_w_args(self)
                                extra.other.func_gui.select_element(self)
                                break
                del self.json_data['Playlists'][current_playlist][i]

            elif type(self.json_data['Playlists'][current_playlist]) == list:
                if i == self.current_track_name:
                    self.current_track_name = self.json_data['Playlists'][current_playlist][
                        self.json_data['Playlists'][current_playlist].index(i) + 1]
                    self.current_track = self.current_track_name
                del self.json_data['Playlists'][current_playlist][self.json_data['Playlists'][current_playlist].index(i)]

            self.tracks_area.takeItem(self.tracks_area.row(k))
            with open('extra/json/data.json', 'w', encoding='utf-8') as f:
                json.dump(extra.other.func_set_change_return_data.data_without_local_playlist(self),
                            f, indent=4, ensure_ascii=False)
            self.track_name_lbl.setText(self.current_track_name)
        except (IndexError, KeyError):
            self.tracks_area.takeItem(self.tracks_area.row(k))
            with open('extra/json/data.json', 'w', encoding='utf-8') as f:
                json.dump(extra.other.func_set_change_return_data.data_without_local_playlist(self),
                            f, indent=4, ensure_ascii=False)
            self.track_name_lbl.setText(self.current_track_name)
            self.logs_listwidget.addItem('IndexError, KeyError')

def create_playlist(self):
    self.new_playlist_name = self.find_track_input.text()
    self.forbidden_names = ['', 'Local', 'Downloads']
    if self.new_playlist_name not in self.forbidden_names and len(self.new_playlist_name.replace(' ', '')):
        with open('extra/json/data.json', 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
        self.json_data['Playlists'][self.new_playlist_name] = {}
        with open('extra/json/data.json', 'w', encoding='utf-8') as f:
            json.dump(extra.other.func_set_change_return_data.data_without_local_playlist(self),
                        f, indent=4, ensure_ascii=False)
        self.playlists.addItem(self.new_playlist_name)

def delete_playlist(self):
    self.removed_playlist = self.playlists.currentItem()
    if self.removed_playlist.text() != 'Downloads' and self.removed_playlist.text() != 'Local':
        with open('extra/json/data.json', 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
        del self.json_data['Playlists'][self.removed_playlist.text()]
        self.playlists.takeItem(self.playlists.row(self.removed_playlist))
        with open('extra/json/data.json', 'w', encoding='utf-8') as f:
            json.dump(extra.other.func_set_change_return_data.data_without_local_playlist(self),
                        f, indent=4, ensure_ascii=False)
        self.tracks_area.clear()

def add_track_to_json(self, playlist_name, track_name, track_path):
    with open('extra/json/data.json', 'r', encoding='utf-8') as f:
        self.json_data = json.load(f)
    self.json_data['Playlists'][playlist_name][track_name] = track_path
    with open('extra/json/data.json', 'w', encoding='utf-8') as f:
        json.dump(extra.other.func_set_change_return_data.data_without_local_playlist(self),
                    f, indent=4, ensure_ascii=False)

def add_playlist_to_json(self, playlist_name):
    with open('extra/json/data.json', 'r', encoding='utf-8') as f:
        self.json_data = json.load(f)
    self.json_data['Playlists'][playlist_name] = {}
    with open('extra/json/data.json', 'w', encoding='utf-8') as f:
        json.dump(extra.other.func_set_change_return_data.data_without_local_playlist(self),
                    f, indent=4, ensure_ascii=False)