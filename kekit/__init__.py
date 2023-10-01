# keKit is a general purpose script collection plugin for Krita.
# Copyright (C) 2023  Kjell Emanuelsson.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from krita import *
from .kekit_docker import keKitDocker
from .ke_grid import keGrid
from .ke_batch import keBatch
from .ke_transforms import keCenter, keFitBounds, keHalve, keDouble

__version__ = '0.1'
__license__ = 'GPLv3+ LGPLv3+'
__author__ = 'Kjell Emanuelsson'
__email__ = 'contact@nulldevice.anonaddy.com'
__url__ = 'https://ke-code.xyz'

instance = Krita.instance()

# Load Extensions (first)
instance.addExtension(keCenter(instance))
instance.addExtension(keGrid(instance))
instance.addExtension(keFitBounds(instance))
instance.addExtension(keHalve(instance))
instance.addExtension(keDouble(instance))
instance.addExtension(keBatch(instance))

# Load Docker (Last)
DOCKER_ID = 'kekit_docker'
dock_widget_factory = DockWidgetFactory(DOCKER_ID,DockWidgetFactoryBase.DockRight,keKitDocker)
instance.addDockWidgetFactory(dock_widget_factory)