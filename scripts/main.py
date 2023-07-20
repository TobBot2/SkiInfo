import typing
from PyQt6.QtWidgets import (QWidget, QLabel, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QStackedWidget)
from PyQt6.QtGui import QFont, QFontDatabase, QImage, QPixmap
from PyQt6.QtCore import Qt
import sys
import json
import map
import ski

SCREEN_SIZE = (800, 480)

with open('data/styles.css', 'r') as f:
    QSS_STYLE = f.read()

class ResortsMenuWindow(QMainWindow):
    def __init__(self, resorts: list[str]):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont('data/Snowman.ttf')
        if (font_id < 0): print('ERROR :: Unable to load font')
        self.snowman_font = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.title_size = { 'x':int(SCREEN_SIZE[0]*0.75), 'y':80}
        self.resort_label_height = 75

        self.resorts = resorts
        self.selected_resort = None
        self.select_key = "-> "
        self.unselected_prefix = "    "

        self.create_gui(resorts)

        self.on_scroll_update_resort(0)

    def create_gui(self, resorts: list[str]) -> None:
        if sys.platform == 'win32':
            # self.resize(SCREEN_SIZE[0], SCREEN_SIZE[1])
            self.setWindowTitle('Ski Info')
            self.setFixedSize(SCREEN_SIZE[0], SCREEN_SIZE[1])
            self.setStyleSheet(QSS_STYLE)
        elif sys.platform == 'linux':
            self.showFullScreen()

        # BEGIN LAYOUT STUFF

        self.title = QLabel("\uf012ki Resorts Men\uf02e")
        self.title.setObjectName("title")
        self.title.setFont(QFont(self.snowman_font, self.title_size['y']))

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
        self.scroll_resorts.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
        label.setFont(QFont(self.snowman_font, int(self.resort_label_height * .4)))
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
    
    def get_selected_resort(self) -> str:
        return self.selected_resort.text()[len(self.unselected_prefix):]
    
class ResortInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont('data/Snowman.ttf')
        if (font_id < 0): print('ERROR :: Unable to load font')
        self.snowman_font = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.create_gui()
    
    def create_gui(self):
        if sys.platform == 'win32':
            # self.resize(SCREEN_SIZE[0], SCREEN_SIZE[1])
            self.setWindowTitle('Ski Info')
            self.setFixedSize(SCREEN_SIZE[0], SCREEN_SIZE[1])
            self.setStyleSheet(QSS_STYLE)
        elif sys.platform == 'linux':
            self.showFullScreen()

        with open('data/image.png', 'rb') as f:
            tmp_img = f.read()

        self.title = QLabel("\uf016histler blackco\uf026")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")
        self.title.setFont(QFont(self.snowman_font, 70))

        self.snowfall_48hrs = QLabel(">test")
        self.snowfall_48hrs.setFont(QFont(self.snowman_font, 40))
        self.snowfall_season = QLabel(">test")
        self.snowfall_season.setFont(QFont(self.snowman_font, 40))
        self.temperature_base_min = QLabel(">test")
        self.temperature_base_min.setFont(QFont(self.snowman_font, 40))
        self.temperature_base_max = QLabel(">test")
        self.temperature_base_max.setFont(QFont(self.snowman_font, 40))
        self.temperature_peak_min = QLabel(">test")
        self.temperature_peak_min.setFont(QFont(self.snowman_font, 40))
        self.temperature_peak_max = QLabel(">test")
        self.temperature_peak_max.setFont(QFont(self.snowman_font, 40))

        info_panel = QVBoxLayout()
        info_panel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_panel.addWidget(self.snowfall_48hrs)
        info_panel.addWidget(self.snowfall_season)
        info_panel.addWidget(self.temperature_base_min)
        info_panel.addWidget(self.temperature_base_max)
        info_panel.addWidget(self.temperature_peak_min)
        info_panel.addWidget(self.temperature_peak_max)

        self.trails_label = QLabel("% Trails")
        self.trails_label.setFont(QFont(self.snowman_font, 20))
        self.trails_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.trails_chart = QLabel()
        self.trails_chart.setObjectName("chart")
        self.trails_chart.setPixmap(QPixmap('data/image.png'))
        self.trails_chart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trails = QVBoxLayout()
        trails.addWidget(self.trails_label)
        trails.addWidget(self.trails_chart)

        self.chairs_label = QLabel("% Lifts")
        self.chairs_label.setFont(QFont(self.snowman_font, 20))
        self.chairs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chairs_chart = QLabel()
        self.chairs_chart.setObjectName("chart")
        self.chairs_chart.setPixmap(QPixmap('data/image.png'))
        self.chairs_chart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chairs = QVBoxLayout()
        chairs.addWidget(self.chairs_label)
        chairs.addWidget(self.chairs_chart)

        charts_hbox = QHBoxLayout()
        charts_hbox.addLayout(trails)
        charts_hbox.addLayout(chairs)

        self.resort_map = QLabel()
        self.resort_map.setObjectName("map")
        self.resort_map.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resort_map.setPixmap(QPixmap('data/map.png'))

        graphics = QVBoxLayout()
        graphics.addWidget(self.resort_map)
        graphics.addLayout(charts_hbox)

        data_panel = QHBoxLayout()
        data_panel.addLayout(info_panel)
        data_panel.addLayout(graphics)

        all_layout = QVBoxLayout()
        all_layout.addWidget(self.title)
        all_layout.addLayout(data_panel)

        all_widget = QWidget()
        all_widget.setLayout(all_layout)
        self.setCentralWidget(all_widget)

    def update_info(self, resort):
        pass
        
class Screen(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()

        self.resorts_menu = ResortsMenuWindow(resorts=resorts)
        self.resort_info = ResortInfoWindow()
        self.addWidget(self.resorts_menu)
        self.addWidget(self.resort_info)

        self.setCurrentWidget(self.resorts_menu)

    def keyPressEvent(self, event):
        super(Screen, self).keyPressEvent(event)

        if self.currentWidget() is self.resorts_menu:
            resort = self.resorts_menu.get_selected_resort()
            self.setCurrentWidget(self.resort_info)
            self.resort_info.update_info(resort)
        else:
            self.setCurrentWidget(self.resorts_menu)


if __name__ == '__main__':
    with open('data/favorite_resorts.json') as f:
        resorts = json.load(f)['data']
    
    app = QApplication(sys.argv)

    screen = Screen()
    screen.show()

    sys.exit(app.exec())