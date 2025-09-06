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
        texture_mode = False
        
        for item in k.findChildren(QtWidgets.QCheckBox):
            if item.text() == "jpg":
                jpg_export = item.isChecked()
            elif item.text() == "T":
                texture_mode = item.isChecked()

        # paths
        file_name = os.path.basename(docName)
        export_name = os.path.splitext(file_name)[0]
        new_dir = os.path.dirname(docName) + "/" + doc.name() + "_batch-export"
        
        if texture_mode:
            # no subdir for texturemode:
            new_dir = os.path.dirname(docName)
        else:
            if (os.path.exists(new_dir)
                    and os.path.isdir(new_dir)):
                pass
            else:
                try:
                    os.makedirs(new_dir)
                except OSError as e:
                    view.showFloatingMessage("Batch Export: Create directory failed! Unsaved file?", app.icon("16_light_warning"), 3000, 1)
                    raise e
        
        # save needed to make sure changes are exported, and too annoying to remember manually
        doc.save()

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
            if texture_mode:
                ep.setProperty("alpha", False)
                ep.setProperty("compression", 0) # faster to just use oxipng/pngcrush etc.
            else:
                ep.setProperty("alpha", True)
                ep.setProperty("compression", 0) # int 0-9
            ep.setProperty("indexed", False)
            ep.setProperty("forceSRGB", False)
            ep.setProperty("interlaced", False)
            ep.setProperty("saveSRGBProfile", False)
            ep.setProperty("transparencyFillcolor", [0,0,0]) # rgb 0-255

        # Groups to Export
        gray_scale_naming = {"b","d","r","m","ao","e", 
                             "bump", "disp", "displacement", "roughness", "rough", "metal", "metallic", "emissive", "mask"}
        # if texture_mode:
            # excluded.extend(gray_scale_naming)
        
        e_t = {"paintlayer", "grouplayer", "clonelayer", "vectorlayer"}
        nodes = [n for n in root_node.childNodes() if n.type() in e_t and n.visible() and n.name().lower() not in excluded]
        total_count = str(len(nodes))
        count = 0

        # Run Batch Export
        doc.setBatchmode(True)
        for n in nodes:
            
            if texture_mode and n.name().lower() in gray_scale_naming:
                continue
            elif texture_mode:
                layerName = export_name + "_" + n.name()
            else:
                layerName = n.name()
                
            layerPath = new_dir + "/" + layerName + exp_type
            for o_n in nodes:
                if o_n != n and o_n.visible():
                    o_n.setVisible(False)
            n.setVisible(True)

            doc.refreshProjection()
            doc.exportImage(layerPath, ep )
            count += 1
            # layerName = export_name + "_" + n.name()
            
        for n in nodes:
            n.setVisible(True)
        doc.setBatchmode(False)
        
        if texture_mode:
            # Run Batch Export...again! in grayscale...
            temp_doc = app.openDocument(docName)
            # app.activeWindow().addView(temp_doc)  # not needed?
            temp_doc.setColorSpace("GRAYA", "U8", "sRGB")
            
            nodes = [n for n in temp_doc.rootNode().childNodes() if n.type() in e_t and n.visible() and n.name().lower() not in excluded]

            temp_doc.setBatchmode(True)
            
            for n in nodes:
                if texture_mode and n.name().lower() in gray_scale_naming:
                    
                    layerName = export_name + "_" + n.name()
                    layerPath = new_dir + "/" + layerName + exp_type
                    
                    for o_n in nodes:
                        if o_n != n and o_n.visible():
                            o_n.setVisible(False)
                            
                    n.setVisible(True)

                    temp_doc.refreshProjection()
                    temp_doc.exportImage(layerPath, ep )
                    count += 1
                
            for n in nodes:
                n.setVisible(True)
                
            temp_doc.setBatchmode(False)
            temp_doc.close()
        
        doc.refreshProjection()
        
        # Summary pop-up (mostly to signal export is done)
        if view is not None:
            msg = " Batch Export: %s / %s " % (str(count), total_count)
            view.showFloatingMessage(msg, app.icon("light_dialog-ok"), 3000, 1)

    def createActions(self, window):
        action = window.createAction("keBatch", "keBatch")
        action.triggered.connect(self.ke_batch)
