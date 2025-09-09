import os
from krita import *
from PyQt5.Qt import QColor


def create_fill(doc, x, y, name, color, alpha, blend):
    info = InfoObject()
    info.setProperty("color", color)
    selection = Selection()
    selection.select(0, 0, x, y, 255)
    fl = doc.createFillLayer(name, "color", info, selection)
    fl.setInheritAlpha(alpha)
    fl.setBlendingMode(blend)
    return fl


def create_channel(doc, sm_group, n, x, y, name, color):
    n.setVisible(True)
    # fl = create_fill(doc, x, y, name + "_fill", color, True, "multiply")
    ch_group = doc.createNode(name + "_ch", "grouplayer")
    ch_group.setInheritAlpha(True)
    ch_group.setBlendingMode("copy_" + name)
    ch_group.addChildNode(n, None)
    # ch_group.addChildNode(fl, None)
    sm_group.addChildNode(ch_group, None)


class ToRGBA(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def make_rgba(self):

        app = Krita.instance()
        doc = app.activeDocument()
        win = app.activeWindow()
        view = win.activeView()
        root = doc.rootNode()
        # node = doc.activeNode()

        dname = doc.fileName()
        dx = doc.width()
        dy = doc.height()

        if not dname:
            dname = "unsaved_file"
        else:
            head, tail = os.path.split(dname)
            dname = tail.split(".")[0]

        # Set mode
        k = win.qwindow().findChild(QtWidgets.QDockWidget, 'kekit_docker')
        create_new_doc = False
        for item in k.findChildren(QtWidgets.QCheckBox):
            if item.toolTip().startswith("New"):
                create_new_doc = item.isChecked()

        # view stores actual selection order?! (too used to blender) :D
        nodes = view.selectedNodes()

        if not nodes:
            # Just in case. Not sure if this is even possible? - Always one layer selected
            view.showFloatingMessage("Invalid selection", app.icon("16_light_warning"), 3000, 1)
            return

        node_len = len(nodes)

        max_ch = 4
        if node_len > max_ch:
            nodes = nodes[:3]
            node_len = max_ch
        channels = ["red", "green", "blue", "alpha"][:node_len]

        # To get RGBA top-down ordered in group
        nodes.reverse()
        channels.reverse()

        # Mode set
        new_bg = None
        if create_new_doc:
            # createDocument(width, height, name, colorSpace, bitDepth, colorProfile, DPI)
            doc = app.createDocument(dx, dy, dname + "_sm", "RGBA", "U8", "", 300.0)
            win.addView(doc)
            app.setActiveDocument(doc)
            root = doc.rootNode()
            new_bg = doc.topLevelNodes()[0]
        else:
            # QoL, for imported grayscale
            doc.setColorSpace("RGBA", "U8", "")
            doc.waitForDone()

        # Create Main Group
        sm_group = doc.createNode(dname + "_sm", "grouplayer")
        root.addChildNode(sm_group, None)
        if new_bg:
            new_bg.remove()

        # Main Group Background
        bg = create_fill(doc, dx, dy, dname + "_sm_bg", "black", False, "normal")
        sm_group.addChildNode(bg, None)

        # Create Channels
        for n, ch in zip(nodes, channels):
            if ch != "alpha":
                if create_new_doc:
                    ch_node = n.duplicate()
                else:
                    ch_node = n
                    n.remove()
                create_channel(doc, sm_group, ch_node, dx, dy, ch, QColor(ch))

        if channels[0] == "alpha":
            if create_new_doc:
                a = nodes[0].duplicate()
            else:
                a = nodes[0]
                a.remove()
            # a.setVisible(False)
            a.setName("makeTM-SplitAlphaMerged")
            sm_group.addChildNode(a, None)
            doc.setActiveNode(a)
            doc.refreshProjection()
            doc.waitForDone()
            app.action('convert_to_transparency_mask').trigger()  # does not work in new doc?!

        # doc.setActiveNode(sm_group)  # does not work on groups?
        doc.refreshProjection()

    def createActions(self, window):
        action = window.createAction("ToRGBA", "ToRGBA")
        action.triggered.connect(self.make_rgba)
