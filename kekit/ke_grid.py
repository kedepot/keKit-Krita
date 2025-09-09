from krita import *


class keGrid(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_grid(self):
        app = Krita.instance()
        doc = app.activeDocument()
        win = app.activeWindow().qwindow()
        # Using docker for variable access
        docker = win.findChild(QtWidgets.QDockWidget, 'GridDocker')
        grid_show = docker.findChild(QtWidgets.QCheckBox, 'chkShowGrid')
        grid_snap = docker.findChild(QtWidgets.QCheckBox, 'chkSnapToGrid')

        # Toggle
        if grid_show.isChecked():
            grid_show.setCheckState(False)
            grid_snap.setCheckState(False)
        else:
            # More hacky docker variables
            k_snapping, k_thirds = None, None
            k = win.findChild(QtWidgets.QDockWidget, 'kekit_docker')
            for item in k.findChildren(QtWidgets.QCheckBox):
                if item.text() == "Snap":
                    k_snapping = item
                elif item.text() == "3rd":
                    k_thirds = item

            # Calc Grid
            if k_thirds.isChecked():
                factor_x = 0.333333
                factor_y = 0.333333
                div = 1
            else:
                factor_x = 0.25
                factor_y = 0.25
                div = 2

            w, h = doc.width(), doc.height()

            # Grab remaining props
            aspect_lock = docker.findChild(QtWidgets.QAbstractButton, 'spacingAspectButton')
            grid_div = docker.findChild(QtWidgets.QWidget, 'intSubdivision')
            x_spacing = docker.findChild(QtWidgets.QWidget, 'intHSpacing')
            y_spacing = docker.findChild(QtWidgets.QWidget, 'intVSpacing')
            new_x, new_y = int(w  * factor_x), int(h * factor_y)
            
            # QoL - auto-remove offset...
            # grid_offset = docker.findChild(QtWidgets.QCheckBox, 'chkOffset')
            offset_x = docker.findChild(QtWidgets.QWidget, 'intXOffset')
            offset_y = docker.findChild(QtWidgets.QWidget, 'intYOffset')
            offset_x.setValue(0)
            offset_y.setValue(0)
            
            # Apply
            # - Aspect lock button cannot be state-checked afaict?
            # -> Brute force work-around: Apply, check if correct, Else "fake-click" & apply again...
            # 1st Try
            x_spacing.setValue(new_x)
            y_spacing.setValue(new_y)

            # Check if the correct values have been applied:
            x_spacing = docker.findChild(QtWidgets.QWidget, 'intHSpacing')
            y_spacing = docker.findChild(QtWidgets.QWidget, 'intVSpacing')
            if x_spacing.value() != new_x or y_spacing.value() != new_y:
                # ...then 2nd try with fake-click
                aspect_lock.click()
                x_spacing.setValue(new_x)
                y_spacing.setValue(new_y)

            # Apply grid settings
            grid_div.setValue(div)
            grid_show.setCheckState(True)
            if k_snapping.isChecked():
                grid_snap.setCheckState(True)


    def createActions(self, window):
        action = window.createAction("keGrid", "keGrid")
        action.triggered.connect(self.ke_grid)
