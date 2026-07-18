from krita import *
from math import ceil, floor

class keGrid(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_grid(self):
        app = Krita.instance()
        doc = app.activeDocument()
        win = app.activeWindow()

        grid_box = win.qwindow().findChild(QtWidgets.QDockWidget, 'GridDocker')
        if not grid_box:
            return
        grid_show = grid_box.findChild(QtWidgets.QCheckBox, 'chkShowGrid')
        grid_snap = grid_box.findChild(QtWidgets.QCheckBox, 'chkSnapToGrid')

        cfg = doc.gridConfig()

        # toggle off
        if grid_show.isChecked():
            grid_show.setChecked(False)
            grid_snap.setChecked(False)
            cfg.setVisible(False)
            cfg.setSnap(False)
            doc.setGridConfig(cfg)
            return

        k = win.qwindow().findChild(QtWidgets.QDockWidget, 'kekit_docker')
        k_thirds = k.findChild(QCheckBox, "grid_thirds").isChecked()
        div_box = k.findChild(QtWidgets.QComboBox, "grid_div")
        # div = div_box.currentData()  # if div_box else 2
        pow2_div = int(div_box.currentData()) if div_box else 2  # 2..128
        pow2_max = 128

        # pow2_div = 2^exp (2->1, 4->2, ..., 128->7)
        exp = int(pow2_div).bit_length() - 1

        if k_thirds:
            div = min(3 ** exp, pow2_max)  # cap to ~same max as pow2
        else:
            div = pow2_div

        dw, dh = doc.width(), doc.height()
        spacing_x = max(1, int(round(dw / float(div))))
        spacing_y = max(1, int(round(dh / float(div))))

        cfg.setType("rectangular")
        cfg.setSpacing(QPoint(spacing_x, spacing_y))
        cfg.setOffset(QPoint(0, 0))

        # subdivs cap at 10,not pow2, so clamping at 8 (or 9)
        denom = 3 if k_thirds else 2
        cap = 9 if k_thirds else 8
        subdiv = min(cap, max(1, int(round(div / denom))))
        cfg.setSubdivision(subdiv)
        
        cfg.setSpacingActiveHorizontal(True)
        cfg.setSpacingActiveVertical(True)
        cfg.setVisible(True)
        cfg.setSnap(True)

        doc.setGridConfig(cfg)

        grid_show.setChecked(True)
        grid_snap.setChecked(True)


    def createActions(self, window):
        action = window.createAction("keGrid", "keGrid", "Tools/Scripts/keKit")
        action.triggered.connect(self.ke_grid)
