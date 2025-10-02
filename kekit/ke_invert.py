from krita import *
from PyQt5.Qt import *


class keInvertGreen(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_invert_green(self):
        app = Krita.instance()
        doc = app.activeDocument()
        node = doc.activeNode()
        parent = node.parentNode() if node.parentNode() else doc.rootNode()

        dw = doc.width()
        dh = doc.height()
        
        new_node = node.duplicate()
        parent.addChildNode(new_node, node)

        inv = app.filter('invert')
        inv.apply(new_node, 0, 0, dw, dh)
        new_node.setBlendingMode("copy_green")
        new_node.mergeDown()

    def createActions(self, window):
        action = window.createAction("keInvertGreen", "keInvertGreen")
        action.triggered.connect(self.ke_invert_green)
