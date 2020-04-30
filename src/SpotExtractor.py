import cv2 as cv
import json
import sys
from src.Spot import Spot
from src.ImageLabel import ImageLabel
from src.SpotListWidget import SpotListWidget
from PySide2.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QPushButton, QHBoxLayout, QWidget, QGridLayout, QGroupBox, QFileDialog, QLineEdit, QVBoxLayout, QScrollArea
from PySide2.QtCore import Qt
from PySide2 import QtGui

lotData = {
    "lotName": "",
    "lotID": 0,
    "spots": []
}

class SpotExtractor(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Spot Extractor")

        menuBar = self.buildMenuBar()
        widget = QWidget(self)
        layout = QGridLayout(widget)

        # Main Image Window
        self.scrollArea = QScrollArea()
        self.imageLabel = ImageLabel(self)
        self.scrollArea.setWidget(self.imageLabel)

        # Text Label for Lot Name
        self.lotNameTextField = QLineEdit()
        self.lotNameTextField.setFixedWidth(300)

        # Spot List
        self.spotList = SpotListWidget(self)

        # Image Box Layout
        imageGroupBox = QGroupBox("Image")
        imageLayout = QHBoxLayout()
        imageLayout.addWidget(self.scrollArea)
        imageGroupBox.setLayout(imageLayout)

        # Spot List Box Layout
        rightGroupBox = QGroupBox()
        rightGroupBox.setMaximumWidth(300)
        rightGroupLayout = QVBoxLayout()

        lotNameGroupBox = QGroupBox("Lot Name")
        lotNameLayout = QHBoxLayout()
        lotNameLayout.addWidget(self.lotNameTextField)
        lotNameGroupBox.setLayout(lotNameLayout)

        spotsGroupBox = QGroupBox("Spot List")
        spotsLayout = QHBoxLayout()
        spotsLayout.addWidget(self.spotList)
        spotsGroupBox.setLayout(spotsLayout)

        rightGroupLayout.addWidget(lotNameGroupBox)
        rightGroupLayout.addWidget(spotsGroupBox)
        rightGroupBox.setLayout(rightGroupLayout)

        # Control Buttons Box Layout
        horizontalGroupBox = QGroupBox("Control Buttons")
        controlButtonLayout = QHBoxLayout()
        checkAllButton = QPushButton("Check All")
        uncheckAllButton = QPushButton("Uncheck All")
        deleteCheckedButton = QPushButton("Delete Checked")
        checkAllButton.clicked.connect(self.checkAll)
        uncheckAllButton.clicked.connect(self.uncheckAll)
        deleteCheckedButton.clicked.connect(self.deleteAllChecked)
        controlButtonLayout.addWidget(checkAllButton)
        controlButtonLayout.addWidget(uncheckAllButton)
        controlButtonLayout.addWidget(deleteCheckedButton)
        horizontalGroupBox.setLayout(controlButtonLayout)

        layout.addWidget(imageGroupBox, 0, 0)
        layout.addWidget(rightGroupBox, 0, 1)
        layout.addWidget(horizontalGroupBox, 1, 0, 1, 2)

        self.setMenuBar(menuBar)
        self.setLayout(layout)
        self.setCentralWidget(widget)

    def buildMenuBar(self):
        menuBar = QMenuBar(self)

        fileMenu = QMenu("File")
        loadImageAction = QAction("Load Image", self)
        loadDataAction = QAction("Load Lot Data", self)
        saveDataAction = QAction("Save Lot Data", self)
        exitAction = QAction("Exit", self)

        # Set Trigger for each Action
        loadImageAction.triggered.connect(self.loadImage)
        loadDataAction.triggered.connect(self.loadData)
        saveDataAction.triggered.connect(self.saveData)
        exitAction.triggered.connect(QtGui.qApp.quit)

        # Add actions to menu
        fileMenu.addAction(loadImageAction)
        fileMenu.addAction(loadDataAction)
        fileMenu.addAction(saveDataAction)
        fileMenu.addAction(exitAction)

        menuBar.addMenu(fileMenu)
        return menuBar

    def loadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
        if fileName:
            mat = cv.imread(fileName, cv.IMREAD_UNCHANGED)
            self.imageLabel.setImage(mat)

    def loadData(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Load JSON Data", "", "JSON Files (*.json)", options=options)
        if fileName:
            f = open(fileName, "r")
            j = json.load(f)
            self.lotNameTextField.setText(j["lotName"])
            for spot in j["spots"]:
                p1 = int(spot["topLeft"][0]), int(spot["topLeft"][1])
                p2 = int(spot["topRight"][0]), int(spot["topRight"][1])
                p3 = int(spot["bottomLeft"][0]), int(spot["bottomLeft"][1])
                p4 = int(spot["bottomRight"][0]), int(spot["bottomRight"][1])
                realID = int(spot["realID"])
                id = int(spot["spotID"])
                s = Spot([p1, p2, p3, p4], realID, id)
                self.spotList.addSpot(s)
            self.imageLabel.resetOriginal()
            self.imageLabel.drawSpots()
            self.imageLabel.updateView()

    def saveData(self):
        lotData["spots"].clear()
        lotData["lotName"] = self.lotNameTextField.text()
        for i in range(len(self.spotList)):
            s = self.spotList.spots[i]
            spotData = {
                "spotID": i,
                "realID": s.realID,
                "topLeft": s.points[0],
                "topRight": s.points[1],
                "bottomLeft": s.points[2],
                "bottomRight": s.points[3],
            }
            lotData["spots"].append(spotData)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save JSON Data", "", "JSON Files (*.json)", options=options)
        if fileName:
            jsonData = json.dumps(lotData, indent=2)
            if not fileName.endswith(".json"):
                fileName = fileName + ".json"
            f = open(fileName, "w")
            f.write(jsonData)
            f.flush()
            f.close()

    def checkAll(self):
        for i in range(len(self.spotList)):
            self.spotList.item(i).setCheckState(Qt.Checked)
        self.imageLabel.resetOriginal()
        self.imageLabel.drawSpots()
        self.imageLabel.updateView()

    def uncheckAll(self):
        for i in range(len(self.spotList)):
            self.spotList.item(i).setCheckState(Qt.Unchecked)
        self.imageLabel.resetOriginal()
        self.imageLabel.updateView()

    def deleteAllChecked(self):
        for i in range(len(self.spotList) - 1, -1, -1):
            if self.spotList.item(i).checkState() == Qt.Checked:
                self.spotList.removeSpot(i)
        self.imageLabel.resetOriginal()
        self.imageLabel.drawSpots()
        self.imageLabel.updateView()


if __name__ == "__main__":
    app = QApplication([])
    window = SpotExtractor()
    window.show()
    sys.exit(app.exec_())

