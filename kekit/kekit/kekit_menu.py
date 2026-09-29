from krita import *
from PyQt5.QtWidgets import QMenu


class keKitMenu(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        parent_action = window.createAction("keKit", "keKit", "tools/scripts")
        parent_action.setMenu(QMenu("keKit", window.qwindow()))
