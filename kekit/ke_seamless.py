from krita import *
from PyQt5.Qt import QImage


def import_to_layer(filename, layer, width, height):
    img = QImage(filename)
    #img = img.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
    img = img.scaled(width, height)  # defaults only!
    if not img.isNull():
        # conversion not needed
        #img.convertToFormat(QImage.Format_RGBA8888)
        #img.convertToFormat(QImage.Format_Grayscale8)
        ptr = img.constBits()
        ptr.setsize(img.byteCount())
        layer.setPixelData(bytes(ptr.asarray()), 0, 0, img.width(), img.height())


class keSeamless(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_seamless(self):
        app = Krita.instance()
        doc = app.activeDocument()
        root = doc.rootNode()
        node = doc.activeNode()
        size = doc.width()
        kpath = os.path.join(app.getAppDataLocation(), "pykrita/kekit/cross_offset_mask.png")
        
        if node is None:
            msg = "Seamless Tiling: No layer selected!?"
            kpath = ""
            print(msg)
            if view is not None:
                view.showFloatingMessage(msg, app.icon("warning"), 3000, 1)
                
        if os.path.exists(kpath):
            # check if in group
            parent = node.parentNode() if node.parentNode() else root
            group = doc.createNode(node.name() + "_TileGroup", "grouplayer")
            parent.addChildNode(group, None)

            # dupe nodes
            dupe = node.duplicate()
            dupe.setName(node.name() + "_offset")

            src_dupe = node.duplicate()
            src_dupe.setName(node.name() + "_masksrc")

            # OFFSET - via pixelByte quadrants copying...
            temp_offset = node.duplicate()  # note: removing later just in case

            dw, dh = doc.width(), doc.height()
            cx, cy = int(dw * 0.5), int(dh * 0.5)

            q1 = temp_offset.pixelData(0, 0, dw, dh)
            q2 = temp_offset.pixelData(cx, 0, dw, dh)
            q3 = temp_offset.pixelData(0, cy, dw, dh)
            q4 = temp_offset.pixelData(cx, cy, dw, dh)

            # remap to offset quadrants - yea, overlapping is hacky ¯\_(ツ)_/¯
            temp_offset.setPixelData(q4, 0, 0, dw, dh)
            temp_offset.setPixelData(q3, cx, 0, dw, cy)
            temp_offset.setPixelData(q2, 0, cy, dw, dh)
            temp_offset.setPixelData(q1, cx, cy, dw, dh)

            # ...and the temp just to make sure it is cropped to bounds
            crop_pd = temp_offset.pixelData(0, 0, dw, dh)
            dupe.setPixelData(crop_pd, 0, 0, dw, dh)
                
            group.addChildNode(dupe, None)
            group.addChildNode(src_dupe, None)

            # CREATE NEW LAYER
            #newLayer = doc.createNode("newLayerName", "paintLayer")
            tmask = doc.createTransparencyMask("co_transp_mask")
            src_dupe.addChildNode(tmask, None) 

            import_to_layer(kpath, tmask, dw, dh)

            doc.refreshProjection()
            temp_offset.remove()
            
        elif view is not None:
            msg = "Seamless Tiling: Path to mask-texture invalid/not found!?"
            print(msg)
            if view is not None:
                view.showFloatingMessage(msg, app.icon("warning"), 3000, 1)

                    
    def createActions(self, window):
        action = window.createAction("keSeamless", "keSeamless")
        action.triggered.connect(self.ke_seamless)
