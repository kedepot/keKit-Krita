from krita import Krita, Extension, ManagedColor
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage


def makediv4(n):
    m = n % 4
    return n if m == 0 else n + (4 - m)


class keAverage(Extension):
    
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_average(self, checked=False):
        app = Krita.instance()
        doc = app.activeDocument()
        win = app.activeWindow()
        view = win.activeView() if win else None
        node = doc.activeNode() if doc else None

        def show_msg(msg):
            if view is not None:
                view.showFloatingMessage(msg, app.icon("warning"), 3000, 1)
            print(msg)

        if doc is None or node is None:
            show_msg("Average: No layer selected!?")
            return

        dw, dh = doc.width(), doc.height()
        parent = node.parentNode()
        
        if node.type() == "grouplayer":
            dup = doc.createNode(node.name() + " Averaged", "paintLayer")
            if parent is not None:
                parent.addChildNode(dup, node)
            else:
                doc.rootNode().addChildNode(dup, node)

            try:
                src_bytes = node.mergedPixelData(0, 0, dw, dh)
            except Exception:
                src_bytes = node.projectionPixelData(0, 0, dw, dh)

            dup.setPixelData(src_bytes, 0, 0, dw, dh)
        else:
            dup = node.duplicate()
            dup.setName(node.name() + " Averaged")
            if parent is not None:
                parent.addChildNode(dup, node)
            else:
                doc.rootNode().addChildNode(dup, node)

        doc.setActiveNode(dup)
        node = dup

        fast = True
        try:
            k = win.qwindow().findChild(QtWidgets.QDockWidget, 'kekit_docker')
            fast = k.findChild(QCheckBox, "avg_opt").isChecked()
        except Exception:
            pass


        mask = None
        sel = doc.selection()
        if sel:
            startx, starty, w, h = sel.x(), sel.y(), sel.width(), sel.height()
            dw_pad = makediv4(dw)
            maskBytes = sel.pixelData(0, 0, dw_pad, dh)
            mask = QImage(maskBytes, dw_pad, dh, QImage.Format_Alpha8)
        else:
            startx, starty, w, h = 0, 0, dw, dh

        if (w * h) < 4096:
            fast = False

        pixelBytes = node.pixelData(0, 0, dw, dh)
        img = QImage(pixelBytes, dw, dh, QImage.Format_RGBA8888)

        stepx, stepy = 1, 1
        if fast:
            if w > 64:
                stepx = max(1, int(w / 64))
            if h > 64:
                stepy = max(1, int(h / 64))

        rs, gs, bs = [], [], []
        endx = startx + w
        endy = starty + h

        for x in range(startx, endx, stepx):
            for y in range(starty, endy, stepy):
                if not img.valid(x, y):
                    continue

                c = img.pixelColor(x, y)

                pixel_selected = True
                if mask is not None and mask.valid(x, y):
                    pixel_selected = mask.pixelColor(x, y).alpha() > 245

                if c.alpha() > 245 and pixel_selected:
                    rs.append(c.red())
                    gs.append(c.green())
                    bs.append(c.blue())

        if not rs:
            show_msg("Average: No opaque pixels found.")
            return

        num = len(rs)
        ar = (sum(rs) / num) / 255.0
        ag = (sum(gs) / num) / 255.0
        ab = (sum(bs) / num) / 255.0

        col = ManagedColor("RGBA", "U8", "")
        col.setComponents((ar, ag, ab, 1.0))
        view.setForeGroundColor(col)

        fill_r = int(ar * 255)
        fill_g = int(ag * 255)
        fill_b = int(ab * 255)
        fill_a = 255

        if sel:
            sx, sy, sw, sh = sel.x(), sel.y(), sel.width(), sel.height()
        else:
            sx, sy, sw, sh = 0, 0, dw, dh

        data = bytearray(node.pixelData(sx, sy, sw, sh))

        mask_data = None
        mask_stride = makediv4(sw)
        if mask is not None:
            mask_data = mask.pixelData(sx, sy, mask_stride, sh)

        for y in range(sh):
            for x in range(sw):
                idx = (y * sw + x) * 4

                selected = True
                if mask_data is not None:
                    midx = y * mask_stride + x
                    selected = mask_data[midx] > 245

                if selected:
                    data[idx + 0] = fill_r
                    data[idx + 1] = fill_g
                    data[idx + 2] = fill_b
                    data[idx + 3] = fill_a

        node.setPixelData(bytes(data), sx, sy, sw, sh)
        doc.refreshProjection()

    def createActions(self, window):
        action = window.createAction("keAverage", "Average", "Tools/Scripts/keKit")
        action.triggered.connect(self.ke_average)
