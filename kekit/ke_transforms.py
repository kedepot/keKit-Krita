from krita import *


def get_node_coords(node):
    # Ret dimensions + center XY
    b = node.bounds()
    nx, ny = b.width(), b.height()
    ncx = b.x() + round(nx/2)
    ncy = b.y() + round(ny/2)
    return nx, ny, ncx, ncy


def center_node(w, h, ncx, ncy, node):
    offset = QPoint(w - ncx, h - ncy)
    pos = node.position()
    node.move(pos.x() + offset.x(), pos.y() + offset.y())


def tf(op):
    app = Krita.instance()
    doc = app.activeDocument()
    dx, dy = doc.width(), doc.height()

    node = doc.activeNode()
    nx, ny, ncx, ncy = get_node_coords(node)

    k = [i for i in app.dockers() if i.objectName() == "kekit_docker"][0]
    cb = [i.currentText() for i in k.findChildren(QtWidgets.QComboBox)][0]

    if op == "halve":
        node.scaleNode(QPoint(ncx, ncy), int(nx*0.5), int(ny*0.5), cb)
    elif op == "double":
        node.scaleNode(QPoint(ncx, ncy), int(nx*2), int(ny*2), cb)
    else:
        # center & fit_bounds
        w, h = int(dx / 2), int(dy / 2)
        
        if op == "center_h":
            center_node(w, h, w, ncy, node)
        elif op == "center_v":
            center_node(w, h, ncx, h, node)
        else:
            center_node(w, h, ncx, ncy, node)

            if op == "fit_bounds":
                k_aspect = None

                for item in k.findChildren(QtWidgets.QCheckBox):
                    if item.text() == "Aspect":
                        k_aspect = item
                        break

                if k_aspect.isChecked():
                    # a little backwards
                    factor = dx / float(nx)
                    xc_y = int((float(ny)*float(factor)))
                    xc_x = dx
                    factor = dy / float(ny)
                    yc_y = dy
                    yc_x = int((float(nx)*float(factor)))

                    if xc_x >= dx and xc_y <= dy:
                        new_x = xc_x
                        new_y = xc_y
                    else:
                        new_x = yc_x
                        new_y = yc_y
                else:
                    new_x, new_y = dx, dy

                node.scaleNode(QPoint(w, h), new_x, new_y, cb)

                # check if krita has "nudged the node" and re-center
                # (scaleNode sometimes offset layer 1px? float/int issue I guess)
                nx, ny, ncx, ncy = get_node_coords(node)
                if w - ncx != 0 or h - ncy != 0:
                    center_node(w, h, ncx, ncy, node)
                    
        # Need something to update move tool selection...
        app.action('deselect').trigger()
        # refresh is not enough
        doc.refreshProjection()


class keCenter(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_center(self):
        tf(op="center")
        
    def createActions(self, window):
        action = window.createAction("keCenter", "keCenter")
        action.triggered.connect(self.ke_center)


class keCenterH(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_center_h(self):
        tf(op="center_h")
        
    def createActions(self, window):
        action = window.createAction("keCenterH", "keCenterH")
        action.triggered.connect(self.ke_center_h)


class keCenterV(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_center_v(self):
        tf(op="center_v")
        
    def createActions(self, window):
        action = window.createAction("keCenterV", "keCenterV")
        action.triggered.connect(self.ke_center_v)


class keFitBounds(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_fit_bounds(self):
        tf(op="fit_bounds")

    def createActions(self, window):
        action = window.createAction("keFitBounds", "keFitBounds")
        action.triggered.connect(self.ke_fit_bounds)


class keHalve(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_halve(self):
        tf(op="halve")

    def createActions(self, window):
        action = window.createAction("keHalve", "keHalve")
        action.triggered.connect(self.ke_halve)


class keDouble(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_double(self):
        tf(op="double")

    def createActions(self, window):
        action = window.createAction("keDouble", "keDouble")
        action.triggered.connect(self.ke_double)
