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
    QCheckBox,
    QSpinBox,
    QToolButton,
)

v = '0.23'

# NOTE: This is the single panel docker variant (no tabs)
# Use: Simply swap the names of the kekit_docker files, so the "kekit_docker.py" is the variant you want

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
        widget.setMinimumSize(342,156)
        max_width = 28  # small boxes
        swidth = int(max_width * 1.65)  # larger boxes
        fwidth = 56  # left side main box special...

        main = QVBoxLayout()
        main.setSpacing(3)
        main.setAlignment(Qt.AlignTop)

        smallfont = QtGui.QFont()
        smallfont.setPointSize(8)

        widget.setLayout(main)

        def separator(text="┊"):
            # sep = QtWidgets.QFrame()  # note: (removed lots of code) -> too annoying,
            # instead, just a label:
            sep = QtWidgets.QLabel(text)
            sep.setAlignment(Qt.AlignCenter)
            sep.setFixedWidth(12)
            return sep

        #
        # DEFINE BUTTONS
        #
        # keGrid
        grid_button = QPushButton("keGrid")
        grid_button.setToolTip("Auto-calculate Image Size Relative Quad Grid")
        self.grid_thirds = QCheckBox("cb_grid_thirds")
        self.grid_thirds.setObjectName("grid_thirds")
        self.grid_thirds.setMaximumWidth(swidth)
        self.grid_thirds.setText('3rd')
        self.grid_thirds.setToolTip("keGrid auto-calculates 'Rule of Thirds' instead of Quad")

        self.grid_div = QtWidgets.QComboBox()
        self.grid_div.setMaximumWidth(swidth)
        self.grid_div.setToolTip("Grid divisions (Note: Subdivisions are half value, capped at 8)\nTDLR: 4 -> 4x4 grid, etc.")
        self.grid_div.setObjectName("grid_div")
        for i in [2**n for n in range(1, 8)]:
            self.grid_div.addItem(str(i), i)
        self.grid_div.setCurrentIndex(1)  # default = 4

        # keBatch
        batch_button = QPushButton("Batch")
        batch_button.setToolTip("Batch Export VISIBLE root LAYERS & GROUPS\n"
                                "Excluding visible root layers & groups named 'fx','fg','bg' & 'background'\n"
                                "(Use to affect each of the exported layers/groups)")
        # Batch Export Textures 
        batch_textures_button = QPushButton("BET")
        # batch_textures_button.setMaximumWidth(max_width)
        batch_textures_button.setToolTip("Batch Export Textures: Autonaming, png only, no subdir. \n"
                                "Alpha: Only with (color) group Trnsp.\nAuto grayscale for non-color layers - see docs for more info")
        # keBatch Option(s)
        self.jpg_export = QCheckBox("jpg_export")
        self.jpg_export.setObjectName("jpg_export")
        self.jpg_export.setFont(smallfont)
        self.jpg_export.setText('JPG')
        self.jpg_export.setChecked(False)
        self.jpg_export.setToolTip("JPG used by keBatch if checked, instead of PNG\n(BET (Texture Mode) ignores JPG opt; PNG only)")

        # Center
        center_button = QPushButton("C")
        # center_button.setMinimumWidth(max_width*4)
        center_button.setToolTip("Places selected layer in the center of the document")
        center_button.setMaximumWidth(max_width)
        
        center_h_button = QPushButton("H")
        center_h_button.setToolTip("Places selected layer in the horizontal center of the document\n(Center from Up/Down only)")
        center_h_button.setMaximumWidth(max_width)
        
        center_v_button = QPushButton("V")
        center_v_button.setToolTip("Places selected layer in the vertical center of the document\n(Center from Left/Right only)")
        center_v_button.setMaximumWidth(max_width)

        # Fit Bounds
        fit_button = QPushButton("Fit")
        # fit_button.setMaximumWidth(swidth)
        fit_button.setToolTip("Stretches selected layer to fit the document bounds")
        
        # Fit Bounds Options
        self.fit_aspect = QCheckBox("Asp")
        self.fit_aspect.setObjectName("fit_aspect")
        self.fit_aspect.setFont(smallfont)
        self.fit_aspect.setChecked(True)
        self.fit_aspect.setToolTip("Aspect ratio is maintained by Fit Bounds if checked")

        # Halve & Double
        halve_button = QPushButton("½")
        halve_button.setToolTip("Scale selected layer 50%")
        halve_button.setMaximumWidth(max_width)
        double_button = QPushButton("x2")
        double_button.setToolTip("Scale selected layer 200%")
        double_button.setMaximumWidth(max_width)
        
        # Tile - just use ArrangeR - (Tile can still be used as shortcut...left the extension in)
        # tile_button = QPushButton("Tile")
        # tile_button.setToolTip("Tile selected (paint) layer\nMakes 4 tiles (Just run again for more tiles!)")
        # tile_button.setMaximumWidth(max_width)
        
        # Seamless Tiling
        seamless_button = QPushButton("SeamT")
        seamless_button.setToolTip("Creates a cross-offset Seamless Tiling group-setup\nTip: Use Wrap-around mode to tweak result")
        # seamless_button.setMaximumWidth(max_width)
        
        # Dupe
        dupe_button = QPushButton("keDupe")
        # dupe_button.setMaximumWidth(max_width)
        dupe_button.setText('Dupe')
        dupe_button.setToolTip(
            "Duplicate selection, or the entire layer if there's no selection, directly into a new layer\n"
            "+ Creates a flattened group copy when used on group(s)")
        
        # Desaturate
        desat_button = QPushButton("keDesat")
        # desat_button.setMaximumWidth(max_width)
        desat_button.setText('Desat')
        desat_button.setToolTip(
            "1-click (assign as shortcut) Desaturate\n"
            "Tip: Also works on groups (creates new merged and desaturated layer)")

        # Average Color
        avg_button = QPushButton("keAverage")
        # avg_button.setMaximumWidth(max_width)
        avg_button.setText('Average')
        avg_button.setToolTip(
            "Average Color in selection OR entire layer if no selection\n"
            "Will ignore transparent pixels - for better average")
        
        self.avg_opt = QCheckBox("avg_fast")
        self.avg_opt.setObjectName("avg_opt")
        self.avg_opt.setText('Fast')
        self.avg_opt.setFont(smallfont)
        self.avg_opt.setChecked(True)
        self.avg_opt.setToolTip(
            "FAST: Avg (On) Limited pixel sample size for substantial speed increase (any image size)\n"
            "ACCURATE: (Off) Avg process every single pixel for more accurate result (slow!)"
        )
        
        # Invert Green Channel
        invgreen_button = QPushButton("keInvertGreen")
        # invgreen_button.setMaximumWidth(max_width)
        invgreen_button.setText('invG')
        invgreen_button.setToolTip("Invert Green Channel of selected layer (normal map)")

        # toRGBA
        RGBA_button = QPushButton("ChPack")
        RGBA_button.setToolTip(
            "Combine SELECTED layers - in SELECTION ORDER as R,G,B,A (Alpha optional) channels\n"
            "combining them into a RGBA channel-packed 'splat map' (aka 'ORM' etc.)\n"
            "Alpha: SplitAlpha export: Select (group) Transp-mask, RMB/SplitAlpha/SaveMerged (See docs)")

        # SeparateORM
        SORM_button = QPushButton("Unpack")
        # SORM_button.setMaximumWidth(max_width)
        SORM_button.setToolTip("Unpack: Extract/clone RGB-channels from active layer into separate groups:\n"
            "Naming: ORM -> Occlusion, Roughness & Mask (color or metal) - Non-Destructive!")

        # ArrangeR - Raster Layer Arrange/Grid layout
        arranger_button = QPushButton("Arrange")
        arranger_button.setMinimumWidth(fwidth)
        arranger_button.setToolTip("Arrange layer(s) (raster,vector etc.) in a grid layout\ndefined by columns & rows values dividing document size\n(For each selected layer, or, duplicate to fill if ONE selected)")
                
        self.arr_col_spin = QSpinBox()
        self.arr_col_spin.setFont(smallfont)
        self.arr_col_spin.setPrefix('Col ')
        self.arr_col_spin.setMinimum(1)
        self.arr_col_spin.setMaximum(1000000)
        self.arr_col_spin.setValue(4)
        self.arr_col_spin.setObjectName("arr_columns")
        self.arr_col_spin.setToolTip("Columns")

        self.arr_row_spin = QSpinBox()
        self.arr_row_spin.setFont(smallfont)
        self.arr_row_spin.setPrefix('Row ')
        self.arr_row_spin.setMinimum(1)
        self.arr_row_spin.setMaximum(1000000)
        self.arr_row_spin.setValue(4)
        self.arr_row_spin.setObjectName("arr_rows")
        self.arr_row_spin.setToolTip("Rows")
        
        self.arr_scale = QCheckBox("Scale")
        self.arr_scale.setFont(smallfont)
        self.arr_scale.setObjectName("arr_scale")
        self.arr_scale.setChecked(True)
        self.arr_scale.setToolTip("Scale: Automatically scale layer(s) to fit the grid cell(s)")
        
        self.arr_group = QCheckBox("Group")
        self.arr_group.setFont(smallfont)
        self.arr_group.setObjectName("arr_group")
        self.arr_group.setChecked(True)
        self.arr_group.setToolTip("Group: Creates a new group and adds arranged nodes")
        
        self.arr_padding_spin = QSpinBox()
        self.arr_padding_spin.setPrefix('Pad ')
        self.arr_padding_spin.setFont(smallfont)
        # self.arr_padding_spin.setSuffix(' px')
        # self.arr_padding_spin.setMaximumWidth(swidth)
        self.arr_padding_spin.setMinimum(0)
        self.arr_padding_spin.setMaximum(1000000)
        self.arr_padding_spin.setValue(0)
        self.arr_padding_spin.setObjectName("arr_padding")
        self.arr_padding_spin.setToolTip("Padding - adding empty PIXELS framing inside the cells\n(Except outer bounds - set together with Margin)")
        
        self.arr_margin_spin = QSpinBox()
        self.arr_margin_spin.setFont(smallfont)
        self.arr_margin_spin.setPrefix('Mgn ')
        # self.arr_margin_spin.setSuffix(' px')
        # self.arr_margin_spin.setMaximumWidth(swidth)
        self.arr_margin_spin.setMinimum(0)
        self.arr_margin_spin.setMaximum(1000000)
        self.arr_margin_spin.setValue(0)
        self.arr_margin_spin.setObjectName("arr_margin")
        self.arr_margin_spin.setToolTip("Outer Margin - adding empty PIXELS (outside/around) grid framing all the cells")
        
        self.arr_fill = QCheckBox("Fill")
        self.arr_fill.setObjectName("arr_fill")
        self.arr_fill.setFont(smallfont)
        self.arr_fill.setChecked(False)
        self.arr_fill.setToolTip("Off: FIT inside cell\nOn: FILL cell (useful for overlapping patterns, else use Crop opt)")
        
        self.arr_crop = QCheckBox("Crop")
        self.arr_crop.setObjectName("arr_crop")
        self.arr_crop.setFont(smallfont)
        self.arr_crop.setChecked(False)
        self.arr_crop.setToolTip("Crop cells (when not using (S)caling, or when using (F)ill option)")

        self.arr_aspect = QCheckBox("Asp")
        self.arr_aspect.setObjectName("arr_aspect")
        self.arr_aspect.setFont(smallfont)
        self.arr_aspect.setChecked(True)
        self.arr_aspect.setToolTip("Maintain layer aspect ratio when scaling - or scale to fit cell.")

        self.arr_anchor = QComboBox()
        self.arr_anchor.setMaximumWidth(64)
        self.arr_anchor.setFont(smallfont)
        self.arr_anchor.setObjectName("arr_anchor")
        self.arr_anchor.setToolTip("Select placement/alignment of the layer inside the grid cell\nNote: May work better with 'Scale' options off.")
        self.arr_anchor.addItem("Center")
        self.arr_anchor.addItem("TopLeft")
        self.arr_anchor.addItem("Top")
        self.arr_anchor.addItem("TopRight")
        self.arr_anchor.addItem("Left")
        self.arr_anchor.addItem("Right")
        self.arr_anchor.addItem("BottomLeft")
        self.arr_anchor.addItem("Bottom")
        self.arr_anchor.addItem("BottomRight")

        # Preferred Pixel (Transform) Process
        scalingCombo_label = QLabel("Method:")
        # scalingCombo_label.setAlignment(Qt.AlignLeft)
        # scalingCombo_label.setFont(smallfont)
        
        self.scalingCombo = QComboBox()
        self.scalingCombo.setFont(smallfont)
        self.scalingCombo.setObjectName("scaling_method")
        self.scalingCombo.setToolTip(
            "Pixel transform method for ½,x2,Fit etc.\n"
            "Default: 'Lanczos3' scaling down & 'Mitchell' scaling up"
            )
        self.scalingCombo.addItem("Default")
        self.scalingCombo.addItem("Mitchell")
        self.scalingCombo.addItem("Lanczos3")
        self.scalingCombo.addItem("Bspline")
        self.scalingCombo.addItem("Bell")
        self.scalingCombo.addItem("Bilinear")
        self.scalingCombo.addItem("Box")
        self.scalingCombo.addItem("Bicubic")
        self.scalingCombo.addItem("Hermite")

        # Snap Layer Bounds to Doc Bounds
        snapbounds_button = QPushButton("BSnap")
        snapbounds_button.setMinimumWidth(fwidth)
        snapbounds_button.setText('BSnap')
        snapbounds_button.setToolTip("Snap Selected Layer (bounds) to (nearest) Document bounds (or center!)\nAssign to shortcut!")
        
        self.snapbounds_grid = QCheckBox("Grid")
        self.snapbounds_grid.setObjectName("bsnap_grid")
        self.snapbounds_grid.setFont(smallfont)
        self.snapbounds_grid.setChecked(True)
        self.snapbounds_grid.setToolTip("Also use Grid (intersections) for bounds snap anchor points")
        
        self.snapbounds_layers = QCheckBox("Bounds")
        self.snapbounds_layers.setObjectName("bsnap_layers")
        self.snapbounds_layers.setFont(smallfont)
        self.snapbounds_layers.setChecked(False)
        self.snapbounds_layers.setToolTip("Also use -other- VISIBLE layers bounds anchor points for bounds snap")
        

        #
        # ASSIGN TO MAIN UI - margins note: (0, 4, 0, 0)  # left top right bottom
        #
        ex, ef = QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        spacing = 2  # gaps between items

#         def sep():
#             sep = QtWidgets.QFrame()
#             sep.setFrameShape(QtWidgets.QFrame.HLine)
#             sep.setFrameShadow(QtWidgets.QFrame.Plain)
#             sep.setLineWidth(1)
#             sep.setPalette(QtWidgets.QApplication.palette())
#             sep.setBackgroundRole(QtGui.QPalette.Shadow)
#             sep.setContentsMargins(2, 8, 2, 8) 
#             return sep
        
        panel = QtWidgets.QWidget()
        # panel.setSizePolicy(ex, ex)
        p1 = QtWidgets.QVBoxLayout(panel)
        p1.setContentsMargins(0,0,0,0)
        # p1.setContentsMargins(0, 4, 0, 0)
        p1.setSpacing(3)
        
        p1_row1 = QHBoxLayout()
        p1_row1.setSpacing(spacing)

        # p1_row1.setAlignment(Qt.AlignLeft)
        
        for w in [center_button, 
                  center_h_button, 
                  center_v_button, 
                  separator(), 
                  halve_button, 
                  double_button, 
                  fit_button, 
                  self.fit_aspect,
                  separator(),
                  self.scalingCombo]:
            w.setSizePolicy(ex, ef)
            p1_row1.addWidget(w, 1)

        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(spacing)
        grid.setVerticalSpacing(0)

        btn_w = arranger_button.sizeHint().width()
        grid.setColumnMinimumWidth(0, btn_w)
        # 1st arranger grid row
        grid.addWidget(arranger_button, 0, 0)
        # grid.addWidget(arranger_button, 0, 0, 2, 1)  # spans rows 0 and 1 in column 0
        # arranger_button.setSizePolicy(arranger_button.sizePolicy().horizontalPolicy(), QtWidgets.QSizePolicy.Expanding)
        grid.addWidget(self.arr_col_spin, 0, 2)
        grid.addWidget(self.arr_row_spin, 0, 4)
        grid.addWidget(self.arr_scale, 0, 5)
        grid.addWidget(self.arr_aspect, 0, 6)
        grid.addWidget(self.arr_anchor, 0, 7, 1, 2)
        # 2nd arranger grid row
        grid.addItem(QtWidgets.QSpacerItem(btn_w, 0, ef, ef), 1, 0)
        grid.addWidget(self.arr_padding_spin, 1, 2)
        grid.addWidget(self.arr_margin_spin, 1, 4)
        grid.addWidget(self.arr_group, 1, 5)
        grid.addWidget(self.arr_fill, 1, 6)
        grid.addWidget(self.arr_crop, 1, 7)
        # min.vertical container for grid layout:
        grid_container = QtWidgets.QWidget()
        grid_container.setLayout(grid)
        grid_container.setMinimumHeight(36)
        
        p1.addLayout(p1_row1)
        # p1.addWidget(grid_container)

        #
        # TAB 2
        #
        # page2 = QtWidgets.QWidget()
        # p2 = QtWidgets.QVBoxLayout(panel)
        # p2.setContentsMargins(0, 4, 0, 0)
        # p2.setSpacing(0)
                
        p2_row1 = QHBoxLayout()
        p2_row1.setSpacing(spacing)
        p2_row1.setAlignment(Qt.AlignLeft)

        
        for w in [dupe_button,
                  seamless_button,
                  separator(), 
                  desat_button, 
                  invgreen_button, 
                  avg_button, 
                  self.avg_opt]:
            w.setSizePolicy(ex, ef)
            p2_row1.addWidget(w, 1)

        p2_row2 = QHBoxLayout()
        p2_row2.setSpacing(spacing)
        p2_row2.setAlignment(Qt.AlignLeft)
        
        
        for w in [RGBA_button, 
                  SORM_button, 
                  separator(), 
                  batch_button, 
                  self.jpg_export, 
                  batch_textures_button]:
            w.setSizePolicy(ex, ef)
            p2_row2.addWidget(w, 1)
        
        p1.addLayout(p2_row1)
        p1.addLayout(p2_row2)

        #
        # TAB 3 : Common settings:
        #
        # page3 = QtWidgets.QWidget()
        # p3 = QtWidgets.QVBoxLayout(panel)
        # p3.setContentsMargins(0, 4, 0, 0)
        # p3.setSpacing(0)

        p3_row1 = QHBoxLayout()
        p3_row1.setSpacing(spacing)

        # p3_row1.addWidget(grid_button)
        # p3_row1.addWidget(self.grid_div)
        # p3_row1.addWidget(self.grid_thirds)
        # p3_row1.addWidget(separator())
        # snapbounds_button,
        # self.snapbounds_grid,
        # self.snapbounds_layers,
        # p3_row1.addWidget(scalingCombo_label)
        # p3_row1.addWidget(self.scalingCombo)
        
        for w in [grid_button, 
                  self.grid_div, 
                  self.grid_thirds, 
                  separator(),
                  snapbounds_button,
                  self.snapbounds_grid,
                  self.snapbounds_layers,
                  # scalingCombo_label,
                  ]:
            w.setSizePolicy(ex, ef)
            p3_row1.addWidget(w, 1)
        
        # p3_row2 = QHBoxLayout()
        # p3_row2.setAlignment(Qt.AlignRight)
        # p3_row2.addWidget(scalingCombo_label, 1, Qt.AlignVCenter)
        # p3_row2.addWidget(self.scalingCombo, 1, Qt.AlignVCenter)
        
        p1.addLayout(p3_row1)
        # p1.addLayout(p3_row2)

        p1.addWidget(grid_container)


        # ADD TABS
        # tabs.addTab(page1, "Transform")
        # tabs.addTab(page2, "Process")
        # tabs.addTab(page3, "Options")
        main.addWidget(panel)
        
        self.setWidget(widget)

        #
        # CONNECT SCRIPTS TO BUTTONS
        #
        button_map = {
            arranger_button: "keArrangeR",
            avg_button: "keAverage",
            batch_button: "keBatch",
            batch_textures_button: "keBatchTextures",
            center_button: "keCenter",
            center_h_button: "keCenterH",
            center_v_button: "keCenterV",
            desat_button: "keDesat",
            double_button: "keDouble",
            dupe_button: "keDupe",
            fit_button: "keFitBounds",
            grid_button: "keGrid",
            halve_button: "keHalve",
            invgreen_button: "keInvertGreen",
            RGBA_button: "ToRGBA",
            SORM_button: "SeparateORM",
            seamless_button: "keSeamless",
            snapbounds_button: "keSnapBounds",
        }

        for button, name in button_map.items():
            button.clicked.connect(lambda checked=False, n=name: ButtonClicked(n))
            
        
    def canvasChanged(self, canvas):
        # notifies when views are added or removed
        pass


def ButtonClicked(cmd):
    Krita.instance().action(cmd).trigger()
