import cv2 as cv
from src.Spot import Spot
from PySide2.QtWidgets import QLabel, QInputDialog, QLineEdit
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtCore import Qt
from PySide2 import QtGui


class ImageLabel(QLabel):

    def __init__(self, mainWindow):
        QLabel.__init__(self)

        self.mainWindow = mainWindow
        self.currPoints = []
        self.original = None
        self.currentMat = None

        self.setMinimumWidth(400)
        self.setMinimumWidth(300)


    def mousePressEvent(self, event):
        if self.currentMat is None:
            return

        x = event.pos().x()
        y = event.pos().y()
        self.currPoints.append((x, y))

        self.drawSpots()
        self.drawConnectedPoints(self.currPoints)
        self.updateView()

        if len(self.currPoints) == 4:
            realID, okPressed = QInputDialog.getInt(self, "Real Spot ID", "What is real ID of the spot?")
            if okPressed:
                s = Spot(self.currPoints, realID, len(self.mainWindow.spotList))
                self.mainWindow.spotList.addSpot(s)
            self.currPoints = []

        self.drawSpots()
        self.drawConnectedPoints(self.currPoints)
        self.updateView()

    def setImage(self, mat):
        self.original = mat
        self.currentMat = mat.copy()
        self.updateView()

    def updateView(self):
        if self.currentMat is None:
            return

        img = QImage(self.currentMat.data, self.currentMat.shape[1], self.currentMat.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(img)
        self.setPixmap(pixmap)
        self.setMinimumHeight(self.currentMat.shape[0])
        self.setMinimumWidth(self.currentMat.shape[1])
        self.setMaximumHeight(self.currentMat.shape[0])
        self.setMaximumWidth(self.currentMat.shape[1])
        self.currentMat = self.original.copy()

    def resetOriginal(self):
        self.currentMat = self.original.copy()

    def drawSpots(self):
        for i in range(len(self.mainWindow.spotList)):
            if self.mainWindow.spotList.item(i).checkState() == Qt.Checked:
                self.drawConnectedPoints(self.mainWindow.spotList.spots[i].points)

    def drawConnectedPoints(self, points):
        if self.currentMat is None:
            return

        size = len(points)
        for i in range(0, size):
            pi = points[i]
            cv.circle(self.currentMat, (pi[0], pi[1]), 1, (0, 255, 0), 2)
            if i > 0:
                cv.line(self.currentMat, points[i], points[i-1], (0, 255, 0))

        if size == 4:
            cv.line(self.currentMat, points[0], points[3], (0, 255, 0))