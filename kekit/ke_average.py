from krita import *
from PyQt5.Qt import *


def makediv4(n):
    m = n % 4
    if m == 0:
        return n
    return n + (4 - m)


class keAverage(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_average(self):
        app = Krita.instance()
        doc = app.activeDocument()
        win = app.activeWindow()
        view = win.activeView()
        node = doc.activeNode()

        if node is None:
            msg = "Average: No layer selected!?"
            if view is not None:
                view.showFloatingMessage(msg, app.icon("warning"), 3000, 1)
            print(msg)
            return

        fast = True
        k = win.qwindow().findChild(QtWidgets.QDockWidget, 'kekit_docker')
        for item in k.findChildren(QtWidgets.QCheckBox):
            if item.text() == "F":
                fast = item.isChecked()

        dw, dh = doc.width(), doc.height()

        mask = None
        sel = doc.selection()
        if sel:
            startx, starty, w, h = sel.x(), sel.y(), sel.width(), sel.height()
            # QnD padding hack for QImage needing padded rows by4 issue - Seems to work?
            dw = makediv4(dw)
            # Selection bytearray->QImage as 'selection mask'
            maskBytes = sel.pixelData(0, 0, dw, dh)
            mask = QImage(maskBytes, dw, dh, QImage.Format_Alpha8)
        else:
            startx, starty, w, h = 0, 0, dw, dh

        # Skip fast-mode for small pixel counts
        force_slow = True if (w * h) < 4096 else False
        if force_slow:
            fast = False

        # Layer Color values
        pixelBytes = node.pixelData(0, 0, dw, dh)
        img = QImage(pixelBytes, dw, dh, QImage.Format_RGBA8888)

        # Fast or Accurate (Fast: Samples stepped/capped 4096 pixels)
        stepx, stepy = 1, 1
        if fast:
            if w > 64:
                stepx = int(w / 64)
            if h > 64:
                stepy = int(h / 64)

        r, g, b = [], [], []
        endx = (startx + w)
        endy = (starty + h)

        # Veeery slow without stepping - better method/opt TBD later:
        for x in range(startx, endx, stepx):
            for y in range(starty, endy, stepy):
                if img.valid(x, y):
                    c = img.pixelColor(x, y)
                    pixel_selected = True
                    if mask:
                        if mask.valid(x, y):
                            pixel_selected = True if mask.pixelColor(x, y).alpha() > 245 else False
                    if c.alpha() > 245 and pixel_selected:
                        b.append(c.red())
                        g.append(c.green())
                        r.append(c.blue())

        if r:
            num = len(r)
            eps = 0.000001
            sr, sg, sb = sum(r), sum(g), sum(b)
            ar = (sr / num + eps) / 255
            ag = (sg / num + eps) / 255
            ab = (sb / num + eps) / 255
            col = ManagedColor("RGBA", "U8", "")
            col.setComponents((ab, ag, ar, 1.0))

            view.setForeGroundColor(col)
            # Need the app.action - since there's no way to add an undo step ow (to use setPixelData)?
            app.action('fill_selection_foreground_color').trigger()
            doc.refreshProjection()

            # TO-DO: Progress display for slow mode? seems pretty tedious...

    def createActions(self, window):
        action = window.createAction("keAverage", "keAverage")
        action.triggered.connect(self.ke_average)
