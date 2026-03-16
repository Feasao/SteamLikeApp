from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap;
import requests

class ImageLoader(QThread):
    image_loaded = pyqtSignal(QPixmap)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        response = requests.get(self.url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.image_loaded.emit(pixmap)

    