import json

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

import numpy as np


class ImageViewWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_ratio = 1.0
        self.m_zoom = 1.0
        self.qimage = None

        self.m_xleft = 0
        self.m_ytop = 0

        self.m_imageWidth = self.width()
        self.m_imageHeight = self.height()

        self.setMouseTracking(True)

        self.m_imgToClientTForm = QtGui.QTransform()
        self.m_clientToImgTForm = QtGui.QTransform()

        self.m_coords = QtCore.QPointF(0, 0)
        self.m_mouseDownPos = QtCore.QPoint()

        label_style = "font-size:24px;font-family:Consolas;" \
            + "color:yellowgreen;border-width:0px;" \
            + "background-color:#77000000"
        self.m_label = QtWidgets.QLabel(self)
        self.m_label.setStyleSheet(label_style)
        self.m_label.setVisible(False)

        self.setStyleSheet("background-color:#303030;")

        self._landmarks = []

    def set_image(self, cv_image: np.ndarray):

        self.qimage = cv_image
        #self.qimage = ImageViewWidget.convert_to_qimage(cv_image)

        if self.qimage:
            self.m_imageWidth = self.qimage.width()
            self.m_imageHeight = self.qimage.height()
            self.calculateZoomFit()

        self.repaint()

    def setZoom(self, value):
        if value < 1E-05:
            value = 1E-05
        self.m_ytop += int(self.m_coords.y() * self.m_ratio * (self.m_zoom - value))
        self.m_xleft += int(self.m_coords.x() * self.m_ratio * (self.m_zoom - value))
        self.m_zoom = value
        self.calculateTransforms()
        self.repaint()

    def calculateZoomFit(self):
        if self.m_imageWidth > 0 and self.m_imageHeight > 0:
            xratio = self.width() / float(self.m_imageWidth)
            yratio = self.height() / float(self.m_imageHeight)
            self.m_ratio = min(xratio, yratio)

            self.setZoom(1.0)

            self.m_xleft = (self.width() - self.m_ratio * self.m_imageWidth) / 2.0
            self.m_ytop = (self.height() - self.m_ratio * self.m_imageHeight) / 2.0
            self.calculateTransforms()

    def calculateTransforms(self):
        self.m_imgToClientTForm.setMatrix(self.m_ratio*self.m_zoom, 0, 0, 0,
                                          self.m_ratio*self.m_zoom, 0, self.m_xleft, self.m_ytop, 1)
        self.m_clientToImgTForm, _ = self.m_imgToClientTForm.inverted()
        
        #self.m_label.setGeometry(max(1.0, self.m_xleft), max(0.0, self.m_ytop), 130, 35)

    @staticmethod
    def convert_to_qimage(cv_image: np.ndarray):
        if cv_image is None:
            return None
        image = cv_image.copy()
        height, width, _ = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage
        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = image.rgbSwapped()
        return image

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QtGui.QPainter(self)
        painter.setBrush(QtGui.QBrush(QtGui.QColor('#333333')))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        if self.qimage:
            painter.setTransform(self.m_imgToClientTForm)
            painter.drawImage(0, 0, self.qimage)
            

    def wheelEvent(self, e):
        b = e.angleDelta().y()
        inc = 1.2 if b > 0 else 1/1.2
        self.setZoom(self.m_zoom * inc)
        super().wheelEvent(e)

    def resizeEvent(self, e):
        self.calculateZoomFit()
        super().resizeEvent(e)

    def mousePressEvent(self, e):
        # Store the position where the mouse was pressed
        self.m_mouseDownPos = e.pos()
        super().mousePressEvent(e)

        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            img_pt = self.m_clientToImgTForm.map(e.pos())
            self._landmarks.append([int(round(img_pt.x())), int(round(img_pt.y()))])
            cb = QtWidgets.QApplication.clipboard()
            cb.clear(mode=cb.Clipboard )
            cb.setText(json.dumps(self._landmarks), mode=cb.Clipboard)

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)

        self.m_coords = self.m_clientToImgTForm.map(e.pos())
        label_text = '[%5d, %5d]' % (int(self.m_coords.x()), int(self.m_coords.y()))
        self.m_label.setVisible(True)
        self.m_label.setText(label_text)
        self.m_label.adjustSize()
        if e.buttons() & QtCore.Qt.LeftButton:
            self.m_xleft -= int((self.m_mouseDownPos.x() - e.x()))
            self.m_ytop -= int((self.m_mouseDownPos.y() - e.y()))
            self.m_mouseDownPos = e.pos()
            self.calculateTransforms()
            self.repaint()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self._landmarks.clear()

    def mouseDoubleClickEvent(self, e):
        super().mouseDoubleClickEvent(e)
        self.calculateZoomFit()
        self.repaint()

    def enterEvent(self, e):
        self.m_label.setVisible(True)

    def leaveEvent(self, e):
        self.m_label.setVisible(False)
