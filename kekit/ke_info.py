from krita import *
from PyQt5.QtWidgets import QWidget, QAction, QMessageBox
from .kekit_docker import v

class keInfo(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_info(self):
        messageBox = QMessageBox()
        messageBox.setInformativeText(Application.version())
        messageBox.setWindowTitle('keKit About')
        messageBox.setText(
            "keKit v\n" 
            ""
            ) % v
        messageBox.setStandardButtons(QMessageBox.Close)
        messageBox.setIcon(QMessageBox.Information)
        messageBox.exec()

    def createActions(self, window):
        action = window.createAction("", "keKit")
        action.triggered.connect(self.ke_info)
