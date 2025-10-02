from krita import *
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFormLayout,
    QListWidget,
    QAbstractItemView,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QWidget,
    QPushButton,
    QAbstractScrollArea,
    QComboBox,
    QMessageBox,
    QCheckBox
)


v = '0.20'


class keKitDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('keKit v' + v)
        self.setupVariables()
        self.setupInterface()

    def setupVariables(self):
        self.applicationName = 'keKit'

    def setupInterface(self):
        # MAIN UI
        widget = QWidget()
        widget.setMinimumSize(332,72)
        max_width = 36
        # widget.setMaximumHeight(64)
        vbox = QVBoxLayout()
        vbox.setSpacing(3)
        # vbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        widget.setLayout(vbox)
        separator = " ┊ "

        # DEFINE BUTTONS

        # keGrid
        grid_button = QPushButton("keGrid")
        grid_button.setToolTip("Auto-calculate Image Size Relative Quad Grid")
        # keGrid Options  - grid snapping is useless w/o layerbounds/center snapping. removed toggle.
        # grid_snap = QCheckBox("cb_grid_snap")
        # grid_snap.setText('Snap')
        # grid_snap.setChecked(True)
        # grid_snap.setToolTip("keGrid also toggles grid snapping on/off")
        grid_thirds = QCheckBox("cb_grid_thirds")
        grid_thirds.setText('3rd')
        grid_thirds.setToolTip("keGrid auto-calculates 'Rule of Thirds' instead of Quad")

        # keBatch
        batch_button = QPushButton("Batch")
        batch_button.setToolTip("Batch Export VISIBLE root LAYERS & GROUPS\n"
                                "Excluding visible root layers & groups named 'fx','fg','bg' & 'background'\n"
                                "(Use to affect each of the exported layers/groups)")
        batch_textures_button = QPushButton("BET")
        batch_textures_button.setToolTip("Batch Export Texture Mode:\n"
                                "Autonaming, png only, no subdir, no alpha\n(+auto grayscale for non-color layers)")
        # keBatch Options
        jpg_export = QCheckBox("jpg_export")
        jpg_export.setText('')
        jpg_export.setChecked(False)
        jpg_export.setToolTip("JPG is used by keBatch if checked, instead of PNG\n(BET (Texture Mode) ignores JPG opt; PNG only)")

        # Center
        center_button = QPushButton("Center")
        center_button.setToolTip("Places selected layer in the center of the document")
        # center_button.setMaximumWidth(max_width)
        center_h_button = QPushButton("H")
        center_h_button.setToolTip("Places selected layer in the horizontal center of the document (only)")
        center_h_button.setMaximumWidth(max_width)
        center_v_button = QPushButton("V")
        center_v_button.setToolTip("Places selected layer in the vertical center of the document (only)")
        center_v_button.setMaximumWidth(max_width)

        # Fit Bounds
        fit_button = QPushButton("Fit Bounds")
        fit_button.setToolTip("Stretches selected layer to fit the document bounds")
        # Fit Bounds Options
        fit_aspect = QCheckBox("cb_fit_aspect")
        fit_aspect.setText('')
        fit_aspect.setChecked(True)
        fit_aspect.setToolTip("Aspect ratio is maintained by Fit Bounds if checked")

        # Halve & Double
        halve_button = QPushButton("½")
        halve_button.setToolTip("Scale selected layer 50%")
        halve_button.setMaximumWidth(max_width)
        double_button = QPushButton("x2")
        double_button.setToolTip("Scale selected layer 200%")
        double_button.setMaximumWidth(max_width)
        
        # Tile
        tile_button = QPushButton("Tile")
        tile_button.setToolTip("Tile selected (paint) layer\nMakes 4 tiles (Just run again for more tiles!)")
        tile_button.setMaximumWidth(max_width)
        
        # Seamless Tiling
        seamless_button = QPushButton("ST")
        seamless_button.setToolTip("Creates a cross-offset Seamless Tiling group-setup\nTip: Use Wrap-around mode to tweak result")
        seamless_button.setMaximumWidth(max_width)
        
        # Preferred Pixel Process
        scalingCombo = QComboBox()
        scalingCombo.setToolTip(
            "Override Default transform scaling method for ½,x2,Fit etc.\n"
            "Default: Lanczos3 scaling down & Mitchell scaling up"
            )
        scalingCombo.addItem("Default")
        scalingCombo.addItem("Mitchell")
        scalingCombo.addItem("Lanczos3")
        scalingCombo.addItem("Bspline")
        scalingCombo.addItem("Bell")
        scalingCombo.addItem("Bilinear")
        scalingCombo.addItem("Box")
        scalingCombo.addItem("Bicubic")
        scalingCombo.addItem("Hermite")

        # Dupe
        dupe_button = QPushButton("keDupe")
        dupe_button.setMaximumWidth(max_width)
        dupe_button.setText('Dup')
        dupe_button.setToolTip(
            "Duplicate selection (or entire layer, if no selection) directly into new layer\n"
            "Tip: Also works on groups (no need to flatten)")
        
        # Desaturate
        desat_button = QPushButton("keDesat")
        desat_button.setMaximumWidth(max_width)
        desat_button.setText('Des')
        desat_button.setToolTip(
            "1-click (assign as shortcut) Desaturate\n"
            "Tip: Also works on groups (creates new merged and desaturated layer)")

        # Average Color
        avg_button = QPushButton("keAverage")
        avg_button.setMaximumWidth(max_width)
        avg_button.setText('Avg')
        avg_button.setToolTip(
            "Average Color in selection OR entire layer if no selection\n"
            "Will ignore transparent pixels - for better average")
        avg_opt = QCheckBox("avg_fast")
        avg_opt.setText('')
        avg_opt.setChecked(True)
        avg_opt.setToolTip(
            "FAST: Avg (On) Limited pixel sample size for substantial speed increase (any image size)\n"
            "ACCURATE: (Off) Avg process every single pixel for more accurate result (slow!)"
        )

        # Invert Green Channel
        invgreen_button = QPushButton("keInvertGreen")
        invgreen_button.setMaximumWidth(max_width)
        invgreen_button.setText('invG')
        invgreen_button.setToolTip("Invert Green Channel of selected layer (normal map)")

        # toRGBA
        RGBA_button = QPushButton("chPack")
        RGBA_button.setToolTip(
            "Combine SELECTED layers - in SELECTION ORDER as R,G,B,A (Alpha optional) channels\n"
            "combining them into a RGBA channel-packed 'splat map' (aka 'ORM' etc.)\n"
            "Alpha: SplitAlpha export: Select (group) Transp-mask, RMB/SplitAlpha/SaveMerged (See docs)")
        new_RGBA = QCheckBox("new_rgba")
        new_RGBA.setText('')
        new_RGBA.setChecked(False)
        new_RGBA.setToolTip("New document is created if checked - for the generated channel packed RGBA group\n"
                            "Note: Does not automate 'Convert to Transp-mask' step in new doc!")

        #
        # DEFINE UI ROWS
        #
        spacing = 1
        h1 = QHBoxLayout()
        h1.setSpacing(spacing)
        h1.setAlignment(Qt.AlignLeft)
        h1.addWidget(center_button)
        h1.addWidget(center_h_button)
        h1.addWidget(center_v_button)
        h1.addWidget(QLabel(separator))
        h1.addWidget(grid_button)
        # h1.addWidget(grid_snap)
        h1.addWidget(grid_thirds)
        h1.addWidget(QLabel(separator))
        h1.addWidget(batch_button)
        h1.addWidget(jpg_export)

        h2 = QHBoxLayout()
        h2.setSpacing(spacing)
        h2.setAlignment(Qt.AlignLeft)
        h2.addWidget(halve_button)
        h2.addWidget(double_button)
        h2.addWidget(fit_button)
        h2.addWidget(fit_aspect)
        h2.addWidget(QLabel(separator))
        h2.addWidget(tile_button)
        h2.addWidget(seamless_button)
        h2.addWidget(QLabel(separator))
        h2.addWidget(scalingCombo)

        h3 = QHBoxLayout()
        h3.setSpacing(spacing)
        h3.setAlignment(Qt.AlignLeft)
        h3.addWidget(dupe_button)
        h3.addWidget(desat_button)
        h3.addWidget(invgreen_button)
        h3.addWidget(avg_button)
        h3.addWidget(avg_opt)
        h3.addWidget(QLabel(separator))
        h3.addWidget(RGBA_button)
        h3.addWidget(new_RGBA)
        h3.addWidget(QLabel(separator))
        # h3.addWidget(batch_button)
        # h3.addWidget(jpg_export)
        # h3.addWidget(QLabel(separator))
        h3.addWidget(batch_textures_button)

        # ASSIGN ROWS TO MAIN UI
        vbox.addLayout(h1)
        vbox.addLayout(h2)
        vbox.addLayout(h3)
        self.setWidget(widget)

        #
        # CONNECT SCRIPTS TO BUTTONS
        #
        avg_button.clicked.connect(partial(ButtonClicked, "keAverage"))
        batch_button.clicked.connect(partial(ButtonClicked, "keBatch"))
        batch_textures_button.clicked.connect(partial(ButtonClicked, "keBatchTextures"))
        center_button.clicked.connect(partial(ButtonClicked, "keCenter"))
        center_h_button.clicked.connect(partial(ButtonClicked, "keCenterH"))
        center_v_button.clicked.connect(partial(ButtonClicked, "keCenterV"))
        desat_button.clicked.connect(partial(ButtonClicked, "keDesat"))
        double_button.clicked.connect(partial(ButtonClicked, "keDouble"))
        dupe_button.clicked.connect(partial(ButtonClicked, "keDupe"))
        fit_button.clicked.connect(partial(ButtonClicked, "keFitBounds"))
        grid_button.clicked.connect(partial(ButtonClicked, "keGrid"))
        halve_button.clicked.connect(partial(ButtonClicked, "keHalve"))
        invgreen_button.clicked.connect(partial(ButtonClicked, "keInvertGreen"))
        RGBA_button.clicked.connect(partial(ButtonClicked, "ToRGBA"))
        seamless_button.clicked.connect(partial(ButtonClicked, "keSeamless"))
        tile_button.clicked.connect(partial(ButtonClicked, "keTile"))
        
    def canvasChanged(self, canvas):
        # notifies when views are added or removed
        pass


def ButtonClicked(cmd):
    Krita.instance().action(cmd).trigger()
