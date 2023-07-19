# import PySimpleGUI as sg
from PyQt6.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QWheelEvent
from PyQt6.QtCore import Qt
import sys
import json
import map
import ski

SCREEN_SIZE = (800, 480)

class ResortsMenuWindow(QMainWindow):
    def __init__(self, resorts: list[str]):
        super().__init__()

        self.title_size = { 'x':int(SCREEN_SIZE[0]*0.75), 'y':80}
        self.resort_label_height = 75

        self.resorts = resorts
        self.selected_resort = None
        self.select_key = "-> "
        self.unselected_prefix = "    "

        self.create_gui(resorts)

    def create_gui(self, resorts: list[str]) -> None:
        if sys.platform == 'win32':
            self.resize(SCREEN_SIZE[0], SCREEN_SIZE[1])
            self.setWindowTitle('Ski Info')
        elif sys.platform == 'linux':
            self.showFullScreen()

        font_id = QFontDatabase.addApplicationFont('data/Snowman.ttf')
        if (font_id < 0): print('ERROR :: Unable to load font')
        self.font = QFontDatabase.applicationFontFamilies(font_id)[0]

        # BEGIN LAYOUT STUFF

        self.title = QLabel("\uf012ki Resorts Men\uf02e")
        self.title.setFont(QFont(self.font, self.title_size['y']))

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.create_resort_label(''))
        self.vbox.addWidget(self.create_resort_label(''))
        self.resort_labels = []
        for i in range(len(resorts)):
            resort = self.create_resort_label(self.unselected_prefix + resorts[i]['name'])
            self.resort_labels.append(resort)
            self.vbox.addWidget(resort)
        self.vbox.addWidget(self.create_resort_label(''))
        self.vbox.addWidget(self.create_resort_label(''))

        vbox_widget = QWidget()
        vbox_widget.setLayout(self.vbox)

        self.scroll_resorts = QScrollArea()
        self.scroll_resorts.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_resorts.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_resorts.setWidget(vbox_widget)
        self.scroll_resorts.verticalScrollBar().valueChanged.connect(self.on_scroll_update_resort)

        title_separator = QVBoxLayout()
        title_separator.addWidget(self.title)
        title_separator.addWidget(self.scroll_resorts)

        container = QWidget()
        container.setLayout(title_separator)

        self.setCentralWidget(container)
    
    def create_resort_label(self, name: str) -> QLabel:
        label = QLabel(name)
        label.setFixedSize(SCREEN_SIZE[0]-40, self.resort_label_height)
        label.setFont(QFont(self.font, int(self.resort_label_height * .4)))
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return label
    
    def on_scroll_update_resort(self, scroll_amount):
        new_selected = self.map_scroll_to_resort(scroll_amount)
        
        if new_selected is not self.selected_resort:
            new_selected.setText(self.select_key + new_selected.text()[len(self.unselected_prefix):])
            if self.selected_resort is not None:
                self.selected_resort.setText(self.unselected_prefix + self.selected_resort.text()[len(self.select_key):])
            self.selected_resort = new_selected


    def map_scroll_to_resort(self, amount: int) -> QLabel:
        scroll_range = (self.resort_label_height/4, len(self.resort_labels) * self.resort_label_height)
        resort_label_indeces_range = (0, len(self.resort_labels) - 1)

        # map
        slope = (resort_label_indeces_range[1] - resort_label_indeces_range[0]) / (scroll_range[1] - scroll_range[0])
        resort_index = int(resort_label_indeces_range[0] + slope * (amount - scroll_range[0]))

        # clamp
        resort_index = 0 if resort_index < 0 else resort_index
        resort_index = len(self.resort_labels)-1 if resort_index > len(self.resort_labels)-1 else resort_index

        return self.resort_labels[resort_index]

if __name__ == '__main__':
    with open('data/favorite_resorts.json') as f:
        resorts = json.load(f)['data']
    
    app = QApplication(sys.argv)
    window = ResortsMenuWindow(resorts=resorts)
    window.show()


    sys.exit(app.exec())