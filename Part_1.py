import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap()
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)
        self.ll = '37.530887,55.703118'
        self.spn = '0.002,0.002'
        self.l_map = 'map'
        self.zoom = 17
        self.map_params = {
            "ll": self.ll,
            # "spn": self.spn,
            "l": self.l_map,
            "z": self.zoom
        }
        self.initUI()
        self.getImage()

    def getImage(self):
        server_static_map = "http://static-maps.yandex.ru/1.x/"
        self.response = requests.get(server_static_map, self.map_params)

        if not self.response:
            print("Ошибка выполнения запроса:")
            print(server_static_map)
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            sys.exit(1)

        self.reload()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        # self.reload()

    def reload(self):
        self.pixmap.loadFromData(self.response.content)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.zoom = self.zoom - 1 if self.zoom > 0 else self.zoom
            self.map_params['z'] = self.zoom
            self.getImage()
            self.reload()

        if event.key() == Qt.Key_PageUp:
            self.zoom = self.zoom + 1 if self.zoom < 17 else self.zoom
            self.map_params['z'] = self.zoom
            self.getImage()
            self.reload()

        if event.key() == Qt.Key_Up:
            new_ll = list(map(float, self.ll.split(',')))
            new_ll[1] += 0.001
            new_ll = list(map(str, new_ll))
            self.ll = ','.join(new_ll)
            self.map_params['ll'] = self.ll
            self.getImage()
            self.reload()

        if event.key() == Qt.Key_Down:
            new_ll = list(map(float, self.ll.split(',')))
            new_ll[1] -= 0.001
            new_ll = list(map(str, new_ll))
            self.ll = ','.join(new_ll)
            self.map_params['ll'] = self.ll
            self.getImage()
            self.reload()

        if event.key() == Qt.Key_Right:
            new_ll = list(map(float, self.ll.split(',')))
            new_ll[0] += 0.001
            new_ll = list(map(str, new_ll))
            self.ll = ','.join(new_ll)
            self.map_params['ll'] = self.ll
            self.getImage()
            self.reload()

        if event.key() == Qt.Key_Left:
            new_ll = list(map(float, self.ll.split(',')))
            new_ll[0] -= 0.001
            new_ll = list(map(str, new_ll))
            self.ll = ','.join(new_ll)
            self.map_params['ll'] = self.ll
            self.getImage()
            self.reload()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
