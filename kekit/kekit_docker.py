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

DOCKER_TITLE = 'keKit v0.1'

class keKitDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.setupVariables()
        self.setupInterface()

    def setupVariables(self):
        self.applicationName = "keKit"

    def setupInterface(self):

        widget = QWidget()
        widget.setMinimumSize(320,60)
        # widget.setMaximumHeight(64)
        v = QVBoxLayout()
        widget.setLayout(v)
        separator = " ┊ "

        # Button def
        grid_button = QPushButton("keGrid")
        grid_button.setToolTip("Auto-calculate Image Size Relative Quad Grid")

        batch_button = QPushButton("keBatch")
        batch_button.setToolTip("Batch Export VISIBLE GROUP FOLDERS\n"
            "Visible root layers & groups named 'fx' & 'background' are excluded\n"
            "(Use to affect the exported groups)")

        center_button = QPushButton("Center")
        center_button.setToolTip("Places selected layer in the center of the document")

        fit_button = QPushButton("Fit Bounds")
        fit_button.setToolTip("Stretches selected layer to fit the document bounds")

        halve_button = QPushButton("½")
        halve_button.setToolTip("Scale selected layer 50%")
        halve_button.setMaximumWidth(40)

        double_button = QPushButton("x2")
        double_button.setToolTip("Scale selected layer 200%")
        double_button.setMaximumWidth(40)

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

        # Var1
        fit_aspect = QCheckBox("cb_fit_aspect")
        fit_aspect.setText('Aspect')
        fit_aspect.setChecked(True)
        fit_aspect.setToolTip("Check: Fit Bounds maintains aspect ratio of the image")
        # Var2
        grid_snap = QCheckBox("cb_grid_snap")
        grid_snap.setText('Snap')
        grid_snap.setChecked(True)
        grid_snap.setToolTip("keGrid also toggles grid snapping on/off")
        # Var3
        grid_thirds = QCheckBox("cb_grid_thirds")
        grid_thirds.setText('3rd')
        grid_thirds.setToolTip("keGrid auto-calculates 'Rule of Thirds' instead of Quad")
        # Var4
        jpg_export = QCheckBox("jpg_export")
        jpg_export.setText('jpg')
        jpg_export.setChecked(False)
        jpg_export.setToolTip("Checked: keBatch uses JPG instead of PNG")

        # Assign button rows
        h1 = QHBoxLayout()
        h1.setSpacing(0)
        # h1.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        h1.addWidget(center_button)
        h1.addWidget(QLabel(separator))
        h1.addWidget(grid_button)
        h1.addWidget(grid_snap)
        h1.addWidget(grid_thirds)
        h1.addWidget(QLabel(separator))
        h1.addWidget(batch_button)
        h1.addWidget(jpg_export)

        h2 = QHBoxLayout()
        h2.setSpacing(0)
        # h2.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        h2.addWidget(halve_button)
        h2.addWidget(double_button)
        h2.addWidget(QLabel(separator))
        h2.addWidget(fit_button)
        h2.addWidget(fit_aspect)
        h2.addWidget(QLabel(separator))
        h2.addWidget(scalingCombo)

        # Assign rows to main
        v.addLayout(h1)
        v.addLayout(h2)
        self.setWidget(widget)

        # Assign scripts to buttons
        grid_button.clicked.connect(partial(ButtonClicked, "keGrid"))
        batch_button.clicked.connect(partial(ButtonClicked, "keBatch"))
        center_button.clicked.connect(partial(ButtonClicked, "keCenter"))
        fit_button.clicked.connect(partial(ButtonClicked, "keFitBounds"))
        halve_button.clicked.connect(partial(ButtonClicked, "keHalve"))
        double_button.clicked.connect(partial(ButtonClicked, "keDouble"))

    def canvasChanged(self, canvas):
        # notifies when views are added or removed
        pass


def ButtonClicked(cmd):
    Krita.instance().action(cmd).trigger()
