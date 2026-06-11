from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import Qt


class DraggablePoint(QGraphicsEllipseItem):

    def __init__(self, x, y, radius=6):

        super().__init__(-radius, -radius, radius * 2, radius * 2)

        self.radius = radius
        self.setPos(x, y)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setZValue(100)

    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionChange:

            scene = self.scene()

            if scene and hasattr(scene, "point_moved"):
                scene.point_moved(self, value)

        return super().itemChange(change, value)