from krita import Krita, Extension

class keDesat(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_desat(self):
        app = Krita.instance()
        doc = app.activeDocument()
        if not doc:
            return

        win = app.activeWindow()
        view = win.activeView() if win else None

        nodes = list(view.selectedNodes()) if view else []
        if not nodes:
            node = doc.activeNode()
            if not node:
                return
            nodes = [node]

        filt = Application.filter("desaturate")
        if not filt:
            return

        def rasterize_to_paint(node, name):
            rect = node.bounds()
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            if w <= 0 or h <= 0:
                return None

            parent = node.parentNode() or doc.rootNode()
            paint = doc.createNode(name, "paintLayer")
            parent.addChildNode(paint, node)

            pixels = node.projectionPixelData(x, y, w, h)
            if not pixels:
                paint.remove()
                return Noneg

            paint.setPixelData(pixels, x, y, w, h)
            return paint

        for node in nodes:
            ntype = node.type()

            if ntype == "paintlayer":
                target = node
            else:
                target = rasterize_to_paint(node, "desat_" + node.name())
                if not target:
                    continue
                node.remove()

            rect = target.bounds()
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            if w > 0 and h > 0:
                filt.apply(target, x, y, w, h)

            doc.refreshProjection()

            # silly hack/workaround to refresh layer thumbnails too
            for node in nodes:
                bm = node.blendingMode()
                node.setBlendingMode("allanon" if bm != "allanon" else "parallel")
                node.setBlendingMode(bm)



    def createActions(self, window):
        action = window.createAction("keDesat", "Desaturate", "Tools/Scripts/keKit")
        action.triggered.connect(self.ke_desat)
