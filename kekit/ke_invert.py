from krita import *
from PyQt5.Qt import *


def find_child_nodes(src_node, name="", recursive=True):
    """ex: store all nodes before & after for comparison when no new nodes are returned (like 'mergeDown')"""
    found_nodes = src_node.findChildNodes(name, recursive)  # blank str name = all
    return set(n.uniqueId() for n in found_nodes)


class keInvertGreen(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def ke_invert_green(self):
        app = Krita.instance()
        doc = app.activeDocument()
        node = doc.activeNode()
        root = doc.rootNode()
        parent = node.parentNode() if node.parentNode() else root

        dw = doc.width()
        dh = doc.height()

        og_child_nodes = find_child_nodes(root)
        og_mode = node.blendingMode()
        new_node = node.duplicate()
        parent.addChildNode(new_node, node)

        inv = app.filter('invert')
        inv.apply(new_node, 0, 0, dw, dh)
        new_node.setBlendingMode("copy_green")
        new_node.mergeDown()

        # get newly merged node and re-apply blending mode...
        child_nodes = find_child_nodes(root)
        merged_node_id = [id for id in child_nodes if id not in og_child_nodes][0]
        merged_node = doc.nodeByUniqueID(merged_node_id)
        merged_node.setBlendingMode(og_mode)

    def createActions(self, window):
        action = window.createAction("keInvertGreen", "Invert Green Channel", "Tools/Scripts/keKit")
        action.triggered.connect(self.ke_invert_green)
