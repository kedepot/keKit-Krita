from krita import *
from PyQt5.QtWidgets import QDockWidget, QCheckBox
import math

ANCHORS = (
    (0.0, 0.0),   # topleft
    (0.5, 0.0),   # top
    (1.0, 0.0),   # topright
    (0.0, 0.5),   # left
    (0.5, 0.5),   # center
    (1.0, 0.5),   # right
    (0.0, 1.0),   # bottomleft
    (0.5, 1.0),   # bottom
    (1.0, 1.0),   # bottomright
)

def anchor_point(x, y, w, h, ax, ay):
    return (x + w * ax, y + h * ay)


def all_visible_nodes(node):
    out = []
    for child in node.childNodes():
        if child.visible():
            out.append(child)
            out.extend(all_visible_nodes(child))
    return out


def grid_targets(doc):
    pts = []

    cfg = doc.gridConfig()
    if not cfg.visible():
        return pts

    spacing = cfg.spacing()
    offset = cfg.offset()

    sx = spacing.x()
    sy = spacing.y()
    ox = offset.x()
    oy = offset.y()

    if sx <= 0 or sy <= 0:
        return pts

    x_start = ox + math.floor((0 - ox) / sx) * sx
    y_start = oy + math.floor((0 - oy) / sy) * sy

    x = x_start
    while x <= doc.width():
        y = y_start
        while y <= doc.height():
            pts.append((float(x), float(y)))
            y += sy
        x += sx

    return pts


def visible_layer_targets(doc, active_node):
    pts = []
    root = doc.rootNode()

    for node in all_visible_nodes(root):
        if node == active_node:
            continue

        b = node.bounds()
        if b.isNull() or b.width() <= 0 or b.height() <= 0:
            continue

        for ax, ay in ANCHORS:
            pts.append(anchor_point(b.x(), b.y(), b.width(), b.height(), ax, ay))

    return pts


class keSnapBounds(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_snap_bounds(self):
        doc = Krita.instance().activeDocument()
        node = doc.activeNode()
        win = Krita.instance().activeWindow()

        k = win.qwindow().findChild(QDockWidget, 'kekit_docker')
        use_grid = k.findChild(QCheckBox, "bsnap_grid").isChecked()
        use_visible_layer_bounds = k.findChild(QCheckBox, "bsnap_layers").isChecked()

        b = node.bounds()
        doc_points = []

        for ax, ay in ANCHORS:
            doc_points.append(anchor_point(0, 0, doc.width(), doc.height(), ax, ay))

        if use_grid:
            doc_points.extend(grid_targets(doc))

        if use_visible_layer_bounds:
            doc_points.extend(visible_layer_targets(doc, node))

        if not doc_points:
            return

        best_dist = None
        best_layer = None
        best_doc = None

        for ax, ay in ANCHORS:
            lx, ly = anchor_point(b.x(), b.y(), b.width(), b.height(), ax, ay)
            for dx, dy in doc_points:
                dist = (lx - dx) ** 2 + (ly - dy) ** 2
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best_layer = (lx, ly)
                    best_doc = (dx, dy)

        if best_doc is None:
            return

        dx = int(round(best_doc[0] - best_layer[0]))
        dy = int(round(best_doc[1] - best_layer[1]))

        node.move(int(node.position().x() + dx), int(node.position().y() + dy))
        doc.refreshProjection()

    def createActions(self, window):
        action = window.createAction("keSnapBounds", "BSnap (Layer Bounds Snap)", "Tools/Scripts/keKit")
        action.triggered.connect(self.ke_snap_bounds)
