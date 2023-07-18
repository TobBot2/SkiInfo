# import PySimpleGUI as sg
from PyQt6.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PyQt6.QtCore import Qt
import sys
import json
import map
import ski

SCREEN_SIZE = (800, 480)

def generate_layout(resorts: list[str]):
    return [
        [sg.Text('Pick A Mountain Resort', justification='center')],
        [sg.Listbox([resorts[i]['name'] for i in range(len(resorts)) ],
                   select_mode='LISTBOX_SELECT_MODE_SINGLE', font=('Arial', 30), size=(20,5)),
         sg.Button("OK", size=(20,10))]
    ]

class ResortsMenuWindow(QMainWindow):
    def __init__(self, resorts: list[str]):
        super().__init__()

        self.create_gui(resorts)

    def create_gui(self, resorts: list[str]):
        if sys.platform == 'win32':
            self.resize(SCREEN_SIZE[0], SCREEN_SIZE[1])
            self.setWindowTitle('Ski Info')
        elif sys.platform == 'linux':
            self.showFullScreen()

        font_id = QFontDatabase.addApplicationFont('data/Snowman.ttf')
        if (font_id < 0): print('ERROR :: Unable to load font')
        font = QFontDatabase.applicationFontFamilies(font_id)[0]

        # BEGIN LAYOUT STUFF

        title_size = { 'x':int(SCREEN_SIZE[0]*0.75), 'y':80}
        title = QLabel("Ski Resorts Menu")
        title.setFont(QFont(font, title_size['y']))
        # title.setGeometry(int(SCREEN_SIZE[0]/2-title_size['x']/2), 10, title_size['x'], title_size['y'])

        vbox = QVBoxLayout()
        for i in range(len(resorts)):
            label = QLabel(resorts[i]['name'])
            label.setFixedSize(SCREEN_SIZE[0]-40, 100)
            label.setFont(QFont(font, 30))
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            vbox.addWidget(label)

        vbox_widget = QWidget()
        vbox_widget.setLayout(vbox)

        scroll_resorts = QScrollArea()
        scroll_resorts.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_resorts.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_resorts.setWidget(vbox_widget)

        title_separator = QVBoxLayout()
        title_separator.addWidget(title)
        title_separator.addWidget(scroll_resorts)

        container = QWidget()
        container.setLayout(title_separator)

        self.setCentralWidget(container)
        

if __name__ == '__main__':
    with open('data/favorite_resorts.json') as f:
        resorts = json.load(f)['data']
    # window = sg.Window('Ski Info', layout=generate_layout(resorts), no_titlebar=True, size=SCREEN_SIZE)
    # while True:
    #     event, values = window.read()
    #     if event in ('OK', 'Quit', sg.WIN_CLOSED):
    #         break
    # window.close(); del window
    
    app = QApplication(sys.argv)
    window = ResortsMenuWindow(resorts=resorts)
    window.show()
    sys.exit(app.exec())