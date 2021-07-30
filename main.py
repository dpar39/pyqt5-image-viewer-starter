"""
Main entry point for the gui application
"""
# pylint: disable=invalid-name

import sys
import logging

from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets

from gui.gui import MainWindow

if __name__ == '__main__':
    # Enable logging
    logger = logging.getLogger()
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
    fh = logging.FileHandler("log.txt")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_formatter)
    logger.addHandler(fh)

    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    app = QtWidgets.QApplication(sys.argv)

    try:
        application = MainWindow()
        desktop = app.desktop()
        screen_rect = desktop.screenGeometry()
        screen_size = screen_rect.size() 
        if screen_size == QSize(1024, 600):
            application.showFullScreen()
        else:
            application.show()
        logger.info('Application started.')
        rc = app.exec()
        logger.info('Application ended with code %d', rc)
        sys.exit(rc)
    except Exception as ex:
        logger.critical('Unahandled exception has ocurred: %s', ex, exc_info=True)
        sys.exit(1)
