from krita import *
import os


class keBatch(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_batch(self):
        app = Krita.instance()
        doc = app.activeDocument()
        win = app.activeWindow()
        view = win.activeView()
        root_node = doc.rootNode()
        docName = doc.fileName()
        excluded = ["fx", "background"]

        if not docName:
            print("Quit?")

        print("\nkeBatch Export Process Started...")

        new_dir = os.path.dirname(docName) + "/" + doc.name() + "_batch-export"

        if (os.path.exists(new_dir)
                and os.path.isdir(new_dir)):
            pass
        else:
            try:
                os.makedirs(new_dir)
            except OSError as e:
                view.showFloatingMessage("Batch Export: Create directory failed! Not saved?", app.icon("16_light_warning"), 3000, 1)
                raise e

        # grab jpg option
        k = win.qwindow().findChild(QtWidgets.QDockWidget, 'kekit_docker')
        jpg_export = False
        for item in k.findChildren(QtWidgets.QCheckBox):
            if item.text() == "jpg":
                jpg_export = item.isChecked()


        # exportImage Export Parameters
        ep = InfoObject()
        if jpg_export:
            exp_type = ".jpg"
            # ep.setProperty("baseline", False)
            # ep.setProperty("exif", False)
            # ep.setProperty("filters", bool(['ToolInfo', 'Anonymizer']))
            # ep.setProperty("forceSRGB", False)
            # ep.setProperty("iptcFalse", False)
            ep.setProperty("is_sRGB", True)
            ep.setProperty("optimize", True)
            # ep.setProperty("progressive", False)
            ep.setProperty("quality", 85) # int (0 to 100)
            # ep.setProperty("saveProfile", False)
            # ep.setProperty("smoothing",  0) # int (0 to 100)
            # ep.setProperty("subsampling", 0) # int (0 to 3)
            ep.setProperty("transparencyFillcolor", [255,255,255]) # rgb 0-255
            # ep.setProperty("xmp", False)
        else:
            exp_type = ".png"
            ep.setProperty("alpha", True)
            ep.setProperty("compression", 0) # int 0-9
            ep.setProperty("indexed", False)
            ep.setProperty("forceSRGB", False)
            ep.setProperty("interlaced", False)
            ep.setProperty("saveSRGBProfile", False)
            ep.setProperty("transparencyFillcolor", [0,0,0]) # rgb 0-255

        # Groups to Export
        nodes = [n for n in root_node.childNodes() if n.type() == "grouplayer" and n.visible() and n.name().lower() not in excluded]
        total_count = str(len(nodes))
        count = 0

        # Run Batch Export
        doc.setBatchmode(True)

        for n in nodes:
            layerName = n.name()
            layerPath = new_dir + "/" + layerName + exp_type
            for o_n in nodes:
                if o_n != n and o_n.visible():
                    o_n.setVisible(False)
            n.setVisible(True)

            doc.refreshProjection()
            doc.exportImage(layerPath, ep )
            count += 1
            # print("Batch Export: %s - %s / %s" % (layerName, str(count), total_count))

        # Finalize
        for n in nodes:
            n.setVisible(True)

        doc.setBatchmode(False)

        # Summary pop-up (mostly to signal export is done)
        if view is not None:
            msg = " Batch Export: %s / %s " % (str(count), total_count)
            view.showFloatingMessage(msg, app.icon("light_dialog-ok"), 3000, 1)

    def createActions(self, window):
        action = window.createAction("keBatch", "keBatch")
        action.triggered.connect(self.ke_batch)
