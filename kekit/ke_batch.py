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
        excluded = ["fx", "background", "fg", "bg"]
        
        print("\nkeBatch Export Process Started...")

        # check options
        k = win.qwindow().findChild(QtWidgets.QDockWidget, 'kekit_docker')
        jpg_export = False
        
        for item in k.findChildren(QtWidgets.QCheckBox):
            if item.toolTip().startswith("JPG"):
                jpg_export = item.isChecked()

        # paths
        file_name = os.path.basename(docName)
        export_name = os.path.splitext(file_name)[0]
        new_dir = os.path.join(os.path.dirname(docName), doc.name() + "_batch-export")

        if (os.path.exists(new_dir)
                and os.path.isdir(new_dir)):
            pass
        else:
            try:
                os.makedirs(new_dir)
            except OSError as e:
                view.showFloatingMessage("Batch Export: Create directory failed! Unsaved file?", app.icon("16_light_warning"), 3000, 1)
                raise e

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
        e_t = {"paintlayer", "grouplayer", "clonelayer", "vectorlayer"}
        nodes = [n for n in root_node.childNodes() if n.type() in e_t and n.visible() and n.name().lower() not in excluded]
        total_count = str(len(nodes))
        count = 0

        # Run Batch Export
        doc.setBatchmode(True)
        
        for n in nodes:
            layerName = n.name()
            layerPath = os.path.join(new_dir, layerName + exp_type)
            
            for o_n in nodes:
                if o_n != n and o_n.visible():
                    o_n.setVisible(False)
            n.setVisible(True)

            doc.refreshProjection()
            doc.exportImage(layerPath, ep )
            count += 1
            
        for n in nodes:
            n.setVisible(True)
        doc.setBatchmode(False)

        doc.refreshProjection()
        
        # Summary pop-up (mostly to signal export is done)
        if view is not None:
            msg = " Batch Export: %s / %s " % (str(count), total_count)
            view.showFloatingMessage(msg, app.icon("light_dialog-ok"), 3000, 1)
        
        
    def createActions(self, window):
        action = window.createAction("keBatch", "keBatch")
        action.triggered.connect(self.ke_batch)


class keBatchTextures(Extension):
    
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_batch_texture_mode(self):
        app = Krita.instance()
        doc = app.activeDocument()
        win = app.activeWindow()
        view = win.activeView()
        root_node = doc.rootNode()
        docName = doc.fileName()
        excluded = ["fx", "background", "fg", "bg"]
        
        print("\nkeBatch (Texture Mode) Export Process Started...")

        # paths
        file_name = os.path.basename(docName)
        export_name = os.path.splitext(file_name)[0]
        new_dir = os.path.dirname(docName)

        # exportImage Export Parameters
        ep = InfoObject()
        exp_type = ".png"
        ep.setProperty("alpha", False)
        ep.setProperty("compression", 0) # faster to just use oxipng/pngcrush etc.
        ep.setProperty("indexed", False)
        ep.setProperty("forceSRGB", False)
        ep.setProperty("interlaced", False)
        ep.setProperty("saveSRGBProfile", False)
        ep.setProperty("transparencyFillcolor", [0,0,0]) # rgb 0-255

        # Groups to Export
        gray_scale_naming = {"b","d","r","m","ao","e", 
                             "bump", "disp", "displacement", "roughness", "rough", "metal", "metallic", "emissive", "mask"}
        
        e_t = {"paintlayer", "grouplayer", "clonelayer", "vectorlayer"}
        nodes = [n for n in root_node.childNodes() if n.type() in e_t and n.visible() and n.name().lower() not in excluded]
        total_count = str(len(nodes))
        count = 0

        # Run Batch Export (for color textures)
        gray_nodes = []
        doc.setBatchmode(True)
        for n in nodes:
            
            if n.name().lower() in gray_scale_naming:
                gray_nodes.append(n)
                continue
            
            layerName = export_name + "_" + n.name()
            layerPath = os.path.join(new_dir, layerName + exp_type)
            
            for o_n in nodes:
                if o_n != n and o_n.visible():
                    o_n.setVisible(False)
            n.setVisible(True)

            doc.refreshProjection()
            doc.exportImage(layerPath, ep )
            count += 1
        doc.setBatchmode(False)

        if gray_nodes:
            # Batch Export...in grayscale...
            temp_doc = app.createDocument(doc.width(), doc.height(), "_tmp", "GRAYA", "U8", "sRGB", doc.resolution())
            for n in gray_nodes:
                dupe = n.duplicate()
                temp_doc.rootNode().addChildNode(dupe, None)
            
            # new nodes (all nodes except auto-created Background node:)
            temp_nodes = [n for n in temp_doc.rootNode().childNodes() if n.name() != "Background"]
            
            temp_doc.setBatchmode(True)
            for n in temp_nodes:
                layerName = export_name + "_" + n.name()
                layerPath = os.path.join(new_dir, layerName + exp_type)
                
                for o_n in temp_nodes:
                    if o_n != n and o_n.visible():
                        o_n.setVisible(False)
                        
                n.setVisible(True)

                temp_doc.refreshProjection()
                temp_doc.exportImage(layerPath, ep )
                count += 1
                
            temp_doc.setBatchmode(False)
            temp_doc.close()
    
        for n in nodes:
            n.setVisible(True)
        doc.refreshProjection()
        
        # Summary pop-up (mostly to signal export is done)
        if view is not None:
            msg = " Batch Export (Texture Mode): %s / %s " % (str(count), total_count)
            view.showFloatingMessage(msg, app.icon("light_dialog-ok"), 3000, 1)
        
    def createActions(self, window):
        action = window.createAction("keBatchTextures", "keBatchTextures")
        action.triggered.connect(self.ke_batch_texture_mode)
