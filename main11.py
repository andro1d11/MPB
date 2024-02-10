# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from extra.other.custom_widgets import *
from extra.other.func_connections_elements import *
from extra.other.func_gui import *
from extra.other.func_other import *
from extra.other.func_player_control import *
from extra.other.func_playlists import *
from extra.other.func_set_change_return_data import *
from extra.other.parsers import *
from extra.other.retranslate_ui import *
from extra.other.rpc import *
from extra.other.setup_ui import *
import sys


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.window = parent
        self.setToolTip(f'MusicPyBox')
        self.hidden_menu = QtWidgets.QMenu(parent)
        elems = ['Next track', 'Prev track', 'Play/pause', 'Settings', 'Exit']
        for i in elems:
            self.hidden_menu.addAction(i, self.menu_clicked)
        self.hidden_menu.setIcon(QtGui.QIcon('extra/imgs/music-notes.png'))
        self.hidden_menu.addSeparator()
        self.setContextMenu(self.hidden_menu)

    def menu_clicked(self):
        action = self.sender().text()
        match action:
            case 'Next track':
                self.window.swith_track('next')
            case 'Prev track':
                self.window.swith_track('prev')
            case 'Play/pause':
                self.window.pause_or_resume()
            case 'Settings':
                self.window.open_settings()
            case 'Exit':
                self.window.close()

    def close(self):
        self.hidden_menu.close()


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.song = ''
        self.Play_Pause = True
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: play_mode(self))
        self.timer.start(1000)

    def setupUi(self, Form):
        setup(self, Form)

    def retranslateUi(self, Form):
        retranslate(self, Form)
    
    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.hide()
        self.is_waiting_connect = False
        self.player.pause()
        try:
            self.server.close()
        except:
            pass
        tray_icon.close()
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('MP3-player, PyQt5')
    window.setupUi(window)
    tray_icon = SystemTrayIcon(QtGui.QIcon(
        'extra/imgs/music-notes.png'), window)
    tray_icon.show()
    window.show()
    sys.exit(app.exec_())
