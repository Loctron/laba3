from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainterPath, QPen
from PyQt5.QtCore import Qt


class MembershipFunctionItem(QGraphicsPathItem):

    def __init__(self, scene, points):
        super().__init__()

        self.scene_ref = scene
        self.points = points

        self.setPen(QPen(Qt.blue, 2))
        self.setZValue(1)

        self.update_path()

    def update_path(self):

        a = self.scene_ref.scene_to_scale(self.points[0].x())
        b = self.scene_ref.scene_to_scale(self.points[1].x())
        c = self.scene_ref.scene_to_scale(self.points[2].x())
        d = self.scene_ref.scene_to_scale(self.points[3].x())

        path = QPainterPath()

        start_scale = self.scene_ref.scale_min
        end_scale = self.scene_ref.scale_max

        step = 0.5  # важно: в шкале, не в сцене

        first = True

        x_prev = None
        y_prev = None

        s = start_scale
        while s <= end_scale:

            mu = self.scene_ref.mu(s, a, b, c, d)

            x = self.scene_ref.scale_to_scene(s)
            y = self.scene_ref.base_y - mu * self.scene_ref.amplitude

            if first:
                path.moveTo(x, y)
                first = False
            else:
                path.lineTo(x, y)

            s += step

        self.setPath(path)