from PyQt5 import QtCore, QtWidgets, QtGui
import pyperclip


# Tracks area list model
class ThumbListWidget(QtWidgets.QListWidget):
    def __init__(self, main_obj, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.main_obj = main_obj

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ThumbListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(ThumbListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if self.main_obj.action == 'playlist':
            if event.mimeData().hasUrls():
                event.setDropAction(QtCore.Qt.CopyAction)
                event.accept()
                links = []
                for url in event.mimeData().urls():
                    links.append(str(url.toLocalFile()))
                self.emit(QtCore.SIGNAL("dropped"), links)
            else:
                event.setDropAction(QtCore.Qt.MoveAction)
                super(ThumbListWidget, self).dropEvent(event)


# Model for recomended tracks in main page
class MainPageCell(QtWidgets.QWidget):
    def __init__(self, track_name, path, parent=None):
        super(MainPageCell, self).__init__()
        self.centralwidget = QtWidgets.QWidget()
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(80, 360, 120, 80))
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(60, 40, 341, 241))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.frame.setStyleSheet(
            "background-color: #181818; color: white; border-radius:15px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(0, 56))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setStyleSheet("color: #B3B3B3; font-size: 25px")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame)
        self.copy_bttn = QtWidgets.QPushButton()
        self.copy_bttn.setText('Скопіювати')
        self.copy_bttn.clicked.connect(
            lambda: pyperclip.copy(self.label_2.text()))
        self.verticalLayout_2.addWidget(self.copy_bttn)
        pixmap = QtGui.QPixmap(path).scaled(140, 140)
        self.label.setPixmap(pixmap)
        self.label_2.setText(track_name)
        self.setLayout(self.verticalLayout_2)

    def update(self, track_name, path):
        path = path.replace('\\', '//')
        pixmap = QtGui.QPixmap(path).scaled(140, 140)
        self.label.setPixmap(pixmap)
        self.label_2.setText(track_name)


# Model for assessment criteria
class RateElement(QtWidgets.QWidget):
    def __init__(self, mainWindow, text, extra_property, max, parent=None):
        super(RateElement, self).__init__()
        self.centralwidget = QtWidgets.QWidget()
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.mainWindow = mainWindow
        self.extra_property = extra_property
        self.text = text
        self.value = 1
        
        self.rate_temp_layout = QtWidgets.QHBoxLayout()
        self.const_lbl = QtWidgets.QLabel(text)
        self.rate_slider = QtWidgets.QSlider()
        self.rate_temp_layout.addWidget(self.const_lbl)
        self.rate_temp_layout.addWidget(self.rate_slider)

        self.rate_temp_layout.setStretch(0, 1)
        self.rate_temp_layout.setStretch(1, 1)
        self.rate_temp_layout.setSpacing(25)

        self.rate_slider.setMinimum(1)
        self.rate_slider.setMaximum(max)
        self.rate_slider.setOrientation(QtCore.Qt.Horizontal)

        self.rate_slider.valueChanged.connect(self.slider_release)
        self.setLayout(self.rate_temp_layout)

    def slider_release(self):
        self.const_lbl.setText(f'{self.text}: {self.rate_slider.value()}')
        self.value = self.rate_slider.value()
        self.mainWindow.rhymes_result_pattern[self.extra_property] = self.rate_slider.value()
        rhymes = self.mainWindow.rhymes_result_pattern['rhymes']
        structure = self.mainWindow.rhymes_result_pattern['structure']
        realization = self.mainWindow.rhymes_result_pattern['realization']
        rizz = self.mainWindow.rhymes_result_pattern['rizz']
        vibe = self.mainWindow.rhymes_result_pattern['vibe']
        hype = self.mainWindow.rhymes_result_pattern['hype']
        result = rhymes + structure + realization + rizz
        vibe_percent = (result / 100) * (vibe * 10)
        result += vibe_percent
        hype_percent = (result / 100) * (hype * 10)
        result += hype_percent
        self.mainWindow.rate_result = result
        self.mainWindow.rate_result_lbl.setText(f'{rhymes} + {structure} + {realization} + {rizz} + {vibe * 10}% + {hype * 10}% = {int(result)} pts')


class RatingCell(QtWidgets.QWidget):
    def __init__(self, mainWindow, track_name, path, rating, parent=None):
        super(RatingCell, self).__init__()
        self.centralwidget = QtWidgets.QWidget()
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.mainWindow = mainWindow
        self.track_name = track_name
        self.path = path
        self.rating = rating

        self.main_hbox_layout = QtWidgets.QHBoxLayout()
        self.track_name_lbl = QtWidgets.QLabel(track_name)
        self.rating_lbl = QtWidgets.QLabel(str(rating))
        self.main_hbox_layout.addWidget(self.track_name_lbl)
        self.main_hbox_layout.addWidget(self.rating_lbl)
        self.setLayout(self.main_hbox_layout)


class PlaylistHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PlaylistHeader, self).__init__()
        self.centralwidget = QtWidgets.QWidget()
        self.widget = QtWidgets.QWidget(self.centralwidget)

        self.pixmap_grid_layout = QtWidgets.QGridLayout()
        self.main_header_layout = QtWidgets.QHBoxLayout()
        self.triple_text_layout = QtWidgets.QVBoxLayout()
        self.header_playlist_lbl = QtWidgets.QLabel()
        self.header_name_lbl = QtWidgets.QLabel()
        self.header_ntracks_lbl = QtWidgets.QLabel()
        self.pixmaps = []

        for i in range(2):
            for j in range(2):
                pix_lbl = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap('extra\imgs\default_pic.jpg').scaled(100, 140)
                pix_lbl.setPixmap(pixmap)
                self.pixmaps.append(pix_lbl)
                self.pixmap_grid_layout.addWidget(pix_lbl, i, j)

        font = QtGui.QFont()
        font.setPointSize(25)
        self.header_name_lbl.setFont(font)
        self.header_name_lbl.setText('name')
        font = QtGui.QFont()
        font.setPointSize(12)
        self.header_playlist_lbl.setFont(font)
        self.header_playlist_lbl.setText('Плейлист')
        self.header_ntracks_lbl.setFont(font)
        self.header_ntracks_lbl.setText('ntracks')
        self.triple_text_layout.addWidget(self.header_playlist_lbl)
        self.triple_text_layout.addWidget(self.header_name_lbl)
        self.triple_text_layout.addWidget(self.header_ntracks_lbl)
        self.main_header_layout.addLayout(self.pixmap_grid_layout)
        self.main_header_layout.addLayout(self.triple_text_layout)
        self.main_header_layout.setStretch(1, 10)
        self.setLayout(self.main_header_layout)
    
    def update(self, pixmap_matrix, name, ntracks):
        i = 0
        for pixmap in pixmap_matrix:
            pixmap = QtGui.QPixmap(pixmap).scaled(140, 100)
            if i == 4:
                break
            self.pixmaps[i].setPixmap(pixmap)
            i += 1
        self.header_name_lbl.setText(name)
        self.header_ntracks_lbl.setText(f'{str(ntracks)}  треків')
