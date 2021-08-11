import datetime
import logging
import urllib.request

from PyQt5.QtCore import QByteArray, QSettings, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow

from gui.main_window_ui import Ui_MainWindow


class LoadImageThread(QThread):
    image_loaded = pyqtSignal(QImage)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        try:
            logging.info('Acquisition started')
            # Load an image
            path = 'http://images.cocodataset.org/val2017/000000397133.jpg'
            url_data = urllib.request.urlopen(path).read()
            img = QImage()
            img.loadFromData(url_data)
            self.image_loaded.emit(img)
            logging.info('Image loading completed')
        except Exception as ex:
            logging.info('Error loading image: %s', ex)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = QSettings('Pardi.dev', 'pyqt5-demo') 

        self.restoreGeometry(self.settings.value("geometry", type=QByteArray))
        self.restoreState(self.settings.value("windowState", type=QByteArray))

        self.load_thread = None
        self.load_image()



    def load_image(self):
        self.measure_start_time = datetime.datetime.now()
        measure_thread = LoadImageThread()
        measure_thread.image_loaded.connect(self.on_image_loaded)
        measure_thread.start()

    @pyqtSlot(QImage)
    def on_image_loaded(self, img):
        self.ui.widgetImageViewer.set_image(img)
        self.update()

    def resizeEvent(self, e):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())