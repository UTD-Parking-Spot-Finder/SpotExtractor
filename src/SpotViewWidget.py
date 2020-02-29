from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap, QImage
from PySide2 import QtGui


class SpotViewWidget(QLabel):

    def __init__(self):
        QLabel.__init__(self)

    def showImage(self, img):
        img = QImage(self.currentMat.data, self.currentMat.shape[1], self.currentMat.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(img)
        self.setPixmap(pixmap)