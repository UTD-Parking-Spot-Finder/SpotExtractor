from PySide2.QtWidgets import QListWidget, QListWidgetItem
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtCore import Qt, QEvent, QObject, SIGNAL
from PySide2 import QtGui


class SpotListWidget(QListWidget):

    def __init__(self, mainWindow):
        QListWidget.__init__(self)
        self.spots = []
        self.setFixedWidth(300)
        self.mainWindow = mainWindow
        self.count = 0
        QObject.connect(self, SIGNAL("itemClicked(QListWidgetItem *)"), self.test)

    def test(self):
        self.mainWindow.imageLabel.resetOriginal()
        self.mainWindow.imageLabel.drawSpots()
        self.mainWindow.imageLabel.updateView()

    def addSpot(self, spot):
        self.spots.append(spot)

        item = QListWidgetItem("Spot " + str(self.count))
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        self.addItem(item)
        self.count += 1

    def removeSpot(self, index):
        self.spots.pop(index)
        self.takeItem(index)

    def __len__(self):
        return len(self.spots)