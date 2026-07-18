from krita import *
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtWidgets import QSpinBox, QDockWidget

def anchor_point(x, y, w, h, align):
    return {
        "topleft": (x, y),
        "top": (x + w / 2.0, y),
        "topright": (x + w, y),
        "left": (x, y + h / 2.0),
        "center": (x + w / 2.0, y + h / 2.0),
        "right": (x + w, y + h / 2.0),
        "bottomleft": (x, y + h),
        "bottom": (x + w / 2.0, y + h),
        "bottomright": (x + w, y + h),
    }.get(align, (x + w / 2.0, y + h / 2.0))


class keArrangeR(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_arranger(self):
        app = Krita.instance()
        win = app.activeWindow()
        view = win.activeView()
        doc = view.document()

        k = win.qwindow().findChild(QDockWidget, 'kekit_docker')
        cols = k.findChild(QSpinBox, "arr_columns").value()
        rows = k.findChild(QSpinBox, "arr_rows").value()
        padding = k.findChild(QSpinBox, "arr_padding").value()
        outer_margin = k.findChild(QSpinBox, "arr_margin").value()
        scale_to_fit = k.findChild(QCheckBox, "arr_scale").isChecked()
        fill_cell = k.findChild(QCheckBox, "arr_fill").isChecked()
        crop_to_cell = k.findChild(QCheckBox, "arr_crop").isChecked()
        align = k.findChild(QComboBox, "arr_anchor").currentText().lower()
        keep_aspect = k.findChild(QCheckBox, "arr_aspect").isChecked()
        # shared with the other scripts:
        strategy = k.findChild(QtWidgets.QComboBox, "scaling_method").currentText()

        slots = rows * cols
        selected = list(view.selectedNodes())
        if not selected:
            raise Exception("No layers selected")

        if len(selected) == 1 and slots > 1:
            node = selected[0]
            parent = node.parentNode() if node.parentNode() else doc.rootNode()
            for _ in range(slots - 1):
                dupe = node.duplicate()
                parent.addChildNode(dupe, None)
                selected.append(dupe)

        selected = selected[:slots]

        doc_w = float(doc.width())
        doc_h = float(doc.height())
        
        usable_w = doc_w - (2 * outer_margin) - ((cols - 1) * padding)
        usable_h = doc_h - (2 * outer_margin) - ((rows - 1) * padding)
        
        cell_w = int(round(usable_w / cols))
        cell_h = int(round(usable_h / rows))

        if cell_w <= 0 or cell_h <= 0:
            raise Exception("Grid size seems invalid")

        def crop_pixels_to_rect(node, rect):
            if node.type() != "paintlayer":
                return None

            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()

            b = node.bounds()
            src_x0 = b.x()
            src_y0 = b.y()
            src_w = b.width()
            src_h = b.height()

            # Early out: no overlap
            left = max(x, src_x0)
            top = max(y, src_y0)
            right = min(x + w, src_x0 + src_w)
            bottom = min(y + h, src_y0 + src_h)

            new_layer = doc.createNode(node.name() + "_crop", "paintlayer")
            parent = node.parentNode()
            parent.addChildNode(new_layer, node)

            if right <= left or bottom <= top:
                new_layer.setPixelData(bytes(w * h * 4), x, y, w, h)
                return new_layer

            # If fully inside cell, just copy the node pixels once into the new layer
            if left == src_x0 and top == src_y0 and right == src_x0 + src_w and bottom == src_y0 + src_h:
                src = node.pixelData(src_x0, src_y0, src_w, src_h)
                new_layer.setPixelData(src, src_x0, src_y0, src_w, src_h)
                return new_layer

            src = node.pixelData(src_x0, src_y0, src_w, src_h)
            if not src:
                new_layer.setPixelData(bytes(w * h * 4), x, y, w, h)
                return new_layer

            result = bytearray(w * h * 4)
            row_bytes = (right - left) * 4

            for yy in range(top, bottom):
                src_off = (yy - src_y0) * src_w * 4 + (left - src_x0) * 4
                dst_off = (yy - y) * w * 4 + (left - x) * 4
                result[dst_off:dst_off + row_bytes] = src[src_off:src_off + row_bytes]

            new_layer.setPixelData(bytes(result), x, y, w, h)
            return new_layer


        for idx, node in enumerate(selected):
            row = idx // cols
            col = idx % cols

            target_left = outer_margin + col * (cell_w + padding)
            target_top = outer_margin + row * (cell_h + padding)
            cell_rect = QRect(
                int(round(target_left)),
                int(round(target_top)),
                int(cell_w),
                int(cell_h)
            )

            b = node.bounds()
            bw = float(b.width())
            bh = float(b.height())

            if scale_to_fit and bw > 0 and bh > 0:
                sx = cell_w / bw
                sy = cell_h / bh

                if not keep_aspect:
                    nx = int(round(bw * sx))
                    ny = int(round(bh * sy))
                    if strategy == "Default":
                        method = "LANCZOS3" if (nx < bw or ny < bh) else "MITCHELL"
                    else:
                        method = strategy
                    try:
                        ncx = int(round(b.x() + bw / 2.0))
                        ncy = int(round(b.y() + bh / 2.0))
                        node.scaleNode(QPoint(ncx, ncy), nx, ny, method)
                    except:
                        pass
                else:
                    s = max(sx, sy) if fill_cell else min(sx, sy)
                    nx = int(round(bw * s))
                    ny = int(round(bh * s))
                    if strategy == "Default":
                        method = "LANCZOS3" if s < 1.0 else "MITCHELL"
                    else:
                        method = strategy
                    if abs(s - 1.0) > 0.0001:
                        try:
                            ncx = int(round(b.x() + bw / 2.0))
                            ncy = int(round(b.y() + bh / 2.0))
                            node.scaleNode(QPoint(ncx, ncy), nx, ny, method)
                        except:
                            pass
            
            b = node.bounds()
            p = node.position()

            anchor_x, anchor_y = anchor_point(cell_rect.x(), cell_rect.y(), cell_rect.width(), cell_rect.height(), align)
            nx, ny = anchor_point(b.x(), b.y(), b.width(), b.height(), align)

            dx = int(round(anchor_x - nx))
            dy = int(round(anchor_y - ny))
            node.move(int(p.x() + dx), int(p.y() + dy))

            if crop_to_cell:
                try:
                    b = node.bounds()
                    if (b.x() >= cell_rect.x() and
                        b.y() >= cell_rect.y() and
                        b.x() + b.width() <= cell_rect.x() + cell_rect.width() and
                        b.y() + b.height() <= cell_rect.y() + cell_rect.height()):
                        continue
                        
                    new_node = crop_pixels_to_rect(node, cell_rect)
                    if new_node:
                        parent = node.parentNode()
                        parent.removeChildNode(node)
                        new_node.setName(node.name())
                        
                except Exception as e:
                    print("Crop failed for node:", node.name(), e)

        doc.refreshProjection()

    
    def createActions(self, window):
        action = window.createAction("keArrangeR", "Arrange", "Tools/Scripts/keKit")
        action.triggered.connect(self.ke_arranger)
