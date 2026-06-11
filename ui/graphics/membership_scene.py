from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QPainterPath
from PyQt5.QtCore import Qt

from ui.graphics.draggable_point import DraggablePoint
from ui.graphics.membership_item import MembershipFunctionItem


class MembershipScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scale_min = 0
        self.scale_max = 100

        self.width_scene = 800
        self.height_scene = 350

        self.setSceneRect(0, 0, self.width_scene, self.height_scene)

        self.base_y = 300
        self.amplitude = 200

        self.term_functions = []

        self.draw_axes()

    # =========================
    # МАТЕМАТИЧЕСКАЯ ФУНКЦИЯ μ(x)
    # =========================
    def mu(self, x, a, b, c, d):

        if x < a or x > d:
            return 0.0

        if a <= x < b:
            return (x - a) / (b - a) if b != a else 1.0

        if b <= x <= c:
            return 1.0

        if c < x <= d:
            return (d - x) / (d - c) if d != c else 1.0

        return 0.0

    # =========================
    # ОСИ
    # =========================
    def draw_axes(self):

        pen = QPen(Qt.black)

        self.addLine(50, self.base_y, 750, self.base_y, pen)
        self.addLine(50, 20, 50, self.base_y, pen)

    def clear_functions(self):
        self.clear()
        self.term_functions.clear()
        self.draw_axes()

    # =========================
    # ШКАЛА
    # =========================
    def scale_to_scene(self, value):
        return 50 + (value / self.scale_max) * 700

    def scene_to_scale(self, x):
        return (x - 50) / 700 * self.scale_max

    # =========================
    # СОЗДАНИЕ ТЕРМОВ
    # =========================
    def build_default_terms(self, term_names):

        self.clear_functions()

        count = len(term_names)
        if count < 2:
            return

        step = self.scale_max / (count - 1)

        for i, name in enumerate(term_names):

            center = i * step

            width = step * 1.0
            plateau = step * 0.3

            a = max(self.scale_min, center - width)
            b = max(self.scale_min, center - plateau)

            c = min(self.scale_max, center + plateau)
            d = min(self.scale_max, center + width)

            self.create_function(name, a, b, c, d)

    def create_function(self, name, a, b, c, d):

        x1 = self.scale_to_scene(a)
        x2 = self.scale_to_scene(b)
        x3 = self.scale_to_scene(c)
        x4 = self.scale_to_scene(d)

        # 🔥 ВСЕ ТОЧКИ НА БАЗОВОЙ ЛИНИИ
        top_y = self.base_y - self.amplitude

        p1 = DraggablePoint(x1, self.base_y)
        p2 = DraggablePoint(x2, top_y)
        p3 = DraggablePoint(x3, top_y)
        p4 = DraggablePoint(x4, self.base_y)

        self.addItem(p1)
        self.addItem(p2)
        self.addItem(p3)
        self.addItem(p4)

        function = MembershipFunctionItem(self, [p1, p2, p3, p4])

        self.addItem(function)

        self.term_functions.append({
            "name": name,
            "points": [p1, p2, p3, p4],
            "item": function
        })

    # =========================
    # ДВИЖЕНИЕ ТОЧЕК
    # =========================
    def point_moved(self, point, new_pos):

        x = max(50, min(new_pos.x(), 750))

        point.setPos(x, point.y())

        self.update_all()
        
    def update_all(self):

        for term in self.term_functions:
            term["item"].update_path()

    # =========================
    # ВАЛИДАЦИЯ
    # =========================
    def validate_term(self, points):

        a = self.scene_to_scale(points[0].x())
        b = self.scene_to_scale(points[1].x())
        c = self.scene_to_scale(points[2].x())
        d = self.scene_to_scale(points[3].x())

        return a <= b <= c <= d

    def validate_all(self):

        return all(self.validate_term(t["points"]) for t in self.term_functions)

    # =========================
    # ДАННЫЕ ДЛЯ БД
    # =========================
    def get_functions_data(self):

        result = []

        for term in self.term_functions:

            p = term["points"]

            result.append({
                "term": term["name"],
                "a": self.scene_to_scale(p[0].x()),
                "b": self.scene_to_scale(p[1].x()),
                "c": self.scene_to_scale(p[2].x()),
                "d": self.scene_to_scale(p[3].x())
            })

        return result