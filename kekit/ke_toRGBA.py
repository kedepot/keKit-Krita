import os
from krita import *
from PyQt5.Qt import QColor, QImage


def create_fill(doc, x, y, name, color, alpha, blend):
    info = InfoObject()
    info.setProperty("color", color)
    selection = Selection()
    selection.select(0, 0, x, y, 255)
    fl = doc.createFillLayer(name, "color", info, selection)
    fl.setInheritAlpha(alpha)
    fl.setBlendingMode(blend)
    return fl


def create_channel(doc, sm_group, n, name):
    n.setVisible(True)
    ch_group = doc.createNode(name + "_ch", "grouplayer")
    ch_group.setInheritAlpha(True)
    ch_group.setBlendingMode("copy_" + name)
    ch_group.addChildNode(n, None)
    sm_group.addChildNode(ch_group, None)


def create_sep_channel(doc, sm_group, n, mode):
    n.setVisible(True)
    n.setInheritAlpha(True)
    n.setBlendingMode(mode)
    sm_group.addChildNode(n, None)


def rgb_to_grayscale(src, tgt, w, h):
    pxd = src.pixelData(0, 0, w, h)
    img = QImage(pxd, w, h, QImage.Format_RGBA8888)
    img.setAlphaChannel(QImage())  # Sets to zero/black (needed when src is not opaque)
    img.convertTo(QImage.Format_Grayscale8)
    ptr = img.constBits()
    ptr.setsize(img.byteCount())
    tgt.setPixelData(bytes(ptr.asarray()), 0, 0, w, h)


def merge_group(doc, n, w, h):
    pixel_array = n.projectionPixelData(0, 0, w, h)
    new_node = doc.createNode(n.name() + '_merged','paintlayer')
    new_node.setPixelData(pixel_array, 0, 0, w, h)
    return new_node


def get_props(app):
        doc = app.activeDocument()
        win = app.activeWindow()
        view = win.activeView()
        root = doc.rootNode()
        dname = doc.fileName()
        dw = doc.width()
        dh = doc.height()
        if not dname:
            dname = "unsaved_file"
        else:
            head, tail = os.path.split(dname)
            dname = tail.split(".")[0]
            
        # Set mode - nah?
        # k = win.qwindow().findChild(QtWidgets.QDockWidget, 'kekit_docker')
        # create_new_doc = k.findChild(QCheckBox, "TBD").isChecked()
        create_new_doc = False
        
        # view stores actual selection order?! (I'm too used to Blender...)
        nodes = view.selectedNodes()
        if not nodes:
            # Just in case. Not sure if this is even possible? - Always one layer selected?
            view.showFloatingMessage("Invalid selection", app.icon("16_light_warning"), 3000, 1)
            return
        return app, doc, win, view, root, dname, dw, dh, create_new_doc, nodes


class ToRGBA(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def make_rgba(self):
        app, doc, win, view, root, dname, dw, dh, create_new_doc, nodes = get_props(Krita.instance())

        node_len = len(nodes)

        max_ch = 4
        if node_len > max_ch:
            nodes = nodes[:3]
            node_len = max_ch
        channels = ["red", "green", "blue", "alpha"][:node_len]

        # ORM detection (simple, no user-errors mitigated...)
        orm_naming= ["ao", "o", "r", "m", "mask", "cm"]
        orm_count = 0
        for n in nodes:
            if n.name().lower() in orm_naming:
                orm_count += 1
        # if orm_count >= 3:  # if 4: alpha "support"
        #     dname = "orm"
        #     suffix = ""

        # To get RGBA top-down ordered in group
        nodes.reverse()
        channels.reverse()

        # Mode set
        new_bg = None
        if create_new_doc:
            # createDocument(width, height, name, colorSpace, bitDepth, colorProfile, DPI)
            doc = app.createDocument(dw, dh, dname + "_orm", "RGBA", "U8", "", 300.0)
            win.addView(doc)
            app.setActiveDocument(doc)
            root = doc.rootNode()
            new_bg = doc.topLevelNodes()[0]
        else:
            # QoL, for imported grayscale
            doc.setColorSpace("RGBA", "U8", "")
            doc.waitForDone()

        # replace local orm/a group if existing alreadh
        if orm_count == 4:
            old_orm = doc.nodeByName("orma")
        else:
            old_orm = doc.nodeByName("orm")
        if old_orm is not None:
            old_orm.remove()

        # Create Main Group
        sm_group = doc.createNode("orm", "grouplayer")
        root.addChildNode(sm_group, None)
        if new_bg:
            new_bg.remove()

        # Main Group Background
        bg = create_fill(doc, dw, dh, "group_background", "black", False, "normal")
        sm_group.addChildNode(bg, None)

        # Create Channels
        for n, ch_name in zip(nodes, channels):
            if ch_name != "alpha":
                if create_new_doc:
                    if n.type() == "grouplayer":
                        ch_node = merge_group(doc, n, dw, dh)
                    else:
                        ch_node = n.duplicate()
                else:
                    ch_node = doc.createCloneLayer(n.name() + '_clone', n)  

                create_channel(doc, sm_group, ch_node, ch_name)

        # 0 is the alpha ch (since list is reversed) - if it exists:
        if channels[0] == "alpha":
            sm_group.setName("orma")
            n = nodes[0]
            if create_new_doc:
                if n.type() == "grouplayer":
                    alpha_node = merge_group(doc, n, dw, dh)
                tmask = doc.createTransparencyMask("a_ch-SplitAlpha_SaveMerged")
                rgb_to_grayscale(alpha_node, tmask, dw, dh)
                sm_group.addChildNode(tmask, None)
            else:
                # alpha tm-mask cannot be clone layer...
                tmask = doc.createCloneLayer('conv2TM_SplitAlpha-SaveMerged', n)
                # tmask = doc.createTransparencyMask("a_ch-SplitAlpha_SaveMerged")  # etc. cannot convert clone to tmask here - manual labour req
                sm_group.addChildNode(tmask, None)

        # doc.setActiveNode(sm_group)  # does not work on groups?
        doc.refreshProjection()

    def createActions(self, window):
        action = window.createAction("ToRGBA", "Channel Pack", "Tools/Scripts/keKit")
        action.triggered.connect(self.make_rgba)


class SeparateORM(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def separate_orm(self):
        app, doc, win, view, root, dname, dw, dh, create_new_doc, nodes = get_props(Krita.instance())
        node = doc.activeNode()
        if not node:
            return
        
        src_name = node.name()
        
        # separate color channel group setup
        r_group = doc.createNode(src_name + "_R", "grouplayer")
        g_group = doc.createNode(src_name + "_G", "grouplayer")
        b_group = doc.createNode(src_name + "_B", "grouplayer")

        # background layers for channels
        bg_r = create_fill(doc, dw, dh, "group_background", "black", False, "normal")
        bg_g = bg_r.duplicate()
        bg_b = bg_r.duplicate()
        r_group.addChildNode(bg_r, None)
        g_group.addChildNode(bg_g, None)
        b_group.addChildNode(bg_b, None)

        # add to root
        root.addChildNode(b_group, None)
        root.addChildNode(g_group, None)
        root.addChildNode(r_group, None)

        # create clone layers for color separation
        red = doc.createCloneLayer(src_name + "_RED", node)
        green = doc.createCloneLayer(src_name + "_GREEN", node)
        blue = doc.createCloneLayer(src_name + "_BLUE", node)
        create_sep_channel(doc, r_group, red, "copy_red")
        create_sep_channel(doc, g_group, green, "copy_green")
        create_sep_channel(doc, b_group, blue, "copy_blue")

        # add desaturation
        desat_r = bg_r.duplicate()
        desat_r.setName("desaturate")
        desat_r.setBlendingMode("saturation_hsv")
        desat_g = desat_r.duplicate()
        desat_b = desat_r.duplicate()
        r_group.addChildNode(desat_r, None)
        g_group.addChildNode(desat_g, None)
        b_group.addChildNode(desat_b, None)
        doc.refreshProjection()

    def createActions(self, window):
        action = window.createAction("SeparateORM", "Separate Channels", "Tools/Scripts/keKit")
        action.triggered.connect(self.separate_orm)
