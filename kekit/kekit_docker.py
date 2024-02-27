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


v = '0.14'


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
        widget.setMinimumSize(320, 60)
        # widget.setMaximumHeight(64)
        vbox = QVBoxLayout()
        vbox.setSpacing(1)
        # vbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        widget.setLayout(vbox)
        separator = " ┊ "

        # DEFINE BUTTONS
        
        # keGrid
        grid_button = QPushButton("keGrid")
        grid_button.setToolTip("Auto-calculate Image Size Relative Quad Grid")
        # Options
        grid_snap = QCheckBox("cb_grid_snap")
        grid_snap.setText('Snap')
        grid_snap.setChecked(True)
        grid_snap.setToolTip("keGrid also toggles grid snapping on/off")
        grid_thirds = QCheckBox("cb_grid_thirds")
        grid_thirds.setText('3rd')
        grid_thirds.setToolTip("keGrid auto-calculates 'Rule of Thirds' instead of Quad")

        # keBatch
        batch_button = QPushButton("keBatch")
        batch_button.setToolTip("Batch Export VISIBLE root LAYERS & GROUPS\n"
                                "Visible root layers & groups named 'fx' & 'background' are excluded\n"
                                "(Use to affect each of the exported layers/groups)")
        # Option
        jpg_export = QCheckBox("jpg_export")
        jpg_export.setText('jpg')
        jpg_export.setChecked(False)
        jpg_export.setToolTip("Checked: keBatch uses JPG instead of PNG")

        # Center
        center_button = QPushButton("Center")
        center_button.setToolTip("Places selected layer in the center of the document")
        center_h_button = QPushButton("H")
        center_h_button.setToolTip("Places selected layer in the horizontal center of the document (only)")
        center_h_button.setMaximumWidth(40)
        center_v_button = QPushButton("V")
        center_v_button.setToolTip("Places selected layer in the vertical center of the document (only)")
        center_v_button.setMaximumWidth(40)
        
        # Fit Bounds
        fit_button = QPushButton("Fit Bounds")
        fit_button.setToolTip("Stretches selected layer to fit the document bounds")
        # Options
        fit_aspect = QCheckBox("cb_fit_aspect")
        fit_aspect.setText('Aspect')
        fit_aspect.setChecked(True)
        fit_aspect.setToolTip("Check: Fit Bounds maintains aspect ratio of the image")

        # Halve & Double
        halve_button = QPushButton("½")
        halve_button.setToolTip("Scale selected layer 50%")
        halve_button.setMaximumWidth(40)
        double_button = QPushButton("x2")
        double_button.setToolTip("Scale selected layer 200%")
        double_button.setMaximumWidth(40)
        
        # Preferred Pixel Process
        scalingCombo = QComboBox()
        scalingCombo.setToolTip("Choose pixel transform processing method (for ½,x2 & Fit Bounds)")
        scalingCombo.addItem("Mitchell")
        scalingCombo.addItem("Lanczos3")
        scalingCombo.addItem("Bspline")
        scalingCombo.addItem("Bell")
        scalingCombo.addItem("Bilinear")
        scalingCombo.addItem("Box")
        scalingCombo.addItem("Bicubic")
        scalingCombo.addItem("Hermite")
        
        # Average Color
        avg_button = QPushButton("keAverage")
        avg_button.setText('AVG')
        avg_button.setToolTip(
            "Average Color in selection OR entire layer if no selection\n"
            "Will ignore transparent pixels - for better average\n"
            "Note: Using a selection = 2-3 undo-steps (action-macro)")
        avg_opt = QCheckBox("avg_fast")
        avg_opt.setText('F')
        avg_opt.setChecked(True)
        avg_opt.setToolTip(
            "Set Average Color processing mode:\n"
            "FAST: (On) Limited pixel sample size for substantial speed increase (any image size)\n"
            "ACCURATE: (Off) Process every single pixel for more accurate result (*Very* slow)"
        )

        # toRGBA
        RGBA_button = QPushButton("toRGBA")
        RGBA_button.setToolTip(
            "Combine SELECTED layers - in SELECTION ORDER for R,G,B,A (Alpha optional)\n"
            "combining them into a RGBA channel-packed 'splat map'\n"
            "Note: To use Alpha you must export with Split-Alpha process. See docs.")
        new_RGBA = QCheckBox("new_rgba")
        new_RGBA.setText('New')
        new_RGBA.setChecked(False)
        new_RGBA.setToolTip("Check: Creates a new document for the generated RGBA group")
        
        #
        # DEFINE UI ROWS
        #
        h1 = QHBoxLayout()
        h1.setSpacing(1)
        # h1.setAlignment(Qt.AlignLeft)
        h1.addWidget(center_button)
        h1.addWidget(center_h_button)
        h1.addWidget(center_v_button)
        h1.addWidget(QLabel(separator))
        h1.addWidget(grid_button)
        h1.addWidget(grid_snap)
        h1.addWidget(grid_thirds)

        h2 = QHBoxLayout()
        h2.setSpacing(1)
        # h2.setAlignment(Qt.AlignLeft)
        h2.addWidget(halve_button)
        h2.addWidget(double_button)
        h2.addWidget(QLabel(separator))
        h2.addWidget(fit_button)
        h2.addWidget(fit_aspect)
        h2.addWidget(QLabel(separator))
        h2.addWidget(scalingCombo)

        h3 = QHBoxLayout()
        h3.setSpacing(1)
        # h3.setAlignment(Qt.AlignLeft)
        h3.addWidget(avg_button)
        h3.addWidget(avg_opt)
        h3.addWidget(QLabel(separator))
        h3.addWidget(RGBA_button)
        h3.addWidget(new_RGBA)
        h3.addWidget(QLabel(separator))
        h3.addWidget(batch_button)
        h3.addWidget(jpg_export)

        # ASSIGN ROWS TO MAIN UI
        vbox.addLayout(h1)
        vbox.addLayout(h2)
        vbox.addLayout(h3)
        self.setWidget(widget)

        #
        # CONNECT SCRIPTS TO BUTTONS
        #
        grid_button.clicked.connect(partial(ButtonClicked, "keGrid"))
        batch_button.clicked.connect(partial(ButtonClicked, "keBatch"))
        center_button.clicked.connect(partial(ButtonClicked, "keCenter"))
        center_h_button.clicked.connect(partial(ButtonClicked, "keCenterH"))
        center_v_button.clicked.connect(partial(ButtonClicked, "keCenterV"))
        fit_button.clicked.connect(partial(ButtonClicked, "keFitBounds"))
        halve_button.clicked.connect(partial(ButtonClicked, "keHalve"))
        double_button.clicked.connect(partial(ButtonClicked, "keDouble"))
        RGBA_button.clicked.connect(partial(ButtonClicked, "ToRGBA"))
        avg_button.clicked.connect(partial(ButtonClicked, "keAverage"))

    def canvasChanged(self, canvas):
        # notifies when views are added or removed
        pass


def ButtonClicked(cmd):
    Krita.instance().action(cmd).trigger()
