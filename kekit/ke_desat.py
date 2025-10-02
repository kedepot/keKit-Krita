from krita import *
from PyQt5.Qt import *


class keDesat(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_desat(self):
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

        # Source Pixels
        pixelBytes = node.projectionPixelData(0, 0, dw, dh)
        img = QImage(pixelBytes, dw, dh, QImage.Format_RGBA8888)
        # Desaturated copy
        des = img.convertToFormat(QImage.Format_Grayscale8)
        des.setAlphaChannel(mask)

        # 'Paste' des on img via QPainter
        painter = QPainter()
        painter.begin(img)
        # painter.setCompositionMode(QPainter.CompositionMode_DestinationAtop)  # no need?
        painter.drawImage(0, 0, img)
        painter.drawImage(0, 0, des)
        painter.end()

        # convert to bits
        ptr = img.constBits()
        ptr.setsize(img.byteCount())

        new_node = doc.createNode('desat_' + node.name(),'paintlayer')
        new_node.setPixelData(bytes(ptr.asarray()), 0, 0, dw, dh)
        parent.addChildNode(new_node, node)
        
        # doing merge for single layer - or there is no undo! (+ we can skip refreshProjection!)
        if node.type() != "grouplayer":
            new_node.mergeDown()

        # refresh overhead adds 1s (at 4k, for me) - but seems to not be needed here
        # doc.refreshProjection()

    def createActions(self, window):
        action = window.createAction("keDesat", "keDesat")
        action.triggered.connect(self.ke_desat)
