from krita import *
from PyQt5.Qt import *


class keDupe(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_dupe(self):
        app = Krita.instance()
        doc = app.activeDocument()
        node = doc.activeNode()

        dw = doc.width()
        dh = doc.height()

        parent = node.parentNode() if node.parentNode() else doc.rootNode()

        # Selection (or entire canvas if none) as alpha mask
        mask = None
        sel = doc.selection()
        if sel:
            maskBytes = sel.pixelData(0, 0, dw, dh)
            mask = QImage(maskBytes, dw, dh, QImage.Format_Alpha8)
        else:
            mask = QImage()

        if node.type() != "grouplayer" and not sel:
            new_node = node.duplicate()
        else:
            # Source Pixels
            pixelBytes = node.projectionPixelData(0, 0, dw, dh)
            img = QImage(pixelBytes, dw, dh, QImage.Format_RGBA8888)
            # Apply alpha mask
            img.setAlphaChannel(mask)
            # Add as new node
            ptr = img.constBits()
            ptr.setsize(img.byteCount())
            new_node = doc.createNode('dupe_' + node.name(),'paintlayer')
            new_node.setPixelData(bytes(ptr.asarray()), 0, 0, dw, dh)

        parent.addChildNode(new_node, node)

        # refresh overhead adds 1s (at 4k, for me) - but seems to not be needed here
        # doc.refreshProjection()

    def createActions(self, window):
        action = window.createAction("keDupe", "keDupe")
        action.triggered.connect(self.ke_dupe)
