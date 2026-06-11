from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QGraphicsView,
    QLabel,
    QMessageBox
)

from database.fuzzy_repository import FuzzyRepository
from ui.graphics.membership_scene import MembershipScene


class MembershipEditorWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.repository = FuzzyRepository()
        self.fuzzy_variable_id = None

        self.scene = MembershipScene()

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Термы"))

        self.term_list = QListWidget()
        layout.addWidget(self.term_list)

        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.build_button = QPushButton("Построить")
        self.save_button = QPushButton("Сохранить")

        layout.addWidget(self.build_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.build_button.clicked.connect(self.build_default_functions)
        self.save_button.clicked.connect(self.save_to_database)

    # 🔥 ВАЖНО: теперь реально задаём переменную
    def load_variable(self, fuzzy_variable_id):

        self.fuzzy_variable_id = fuzzy_variable_id

        self.term_list.clear()

        terms = self.repository.get_terms(fuzzy_variable_id)

        for term in terms:
            self.term_list.addItem(term["name"])

    def build_default_functions(self):

        terms = []

        for i in range(self.term_list.count()):
            item = self.term_list.item(i)
            if item:
                terms.append(item.text())

        if not terms:
            QMessageBox.warning(self, "Ошибка", "Нет термов")
            return

        self.scene.build_default_terms(terms)

    def save_to_database(self):

        if self.fuzzy_variable_id is None:
            QMessageBox.warning(self, "Ошибка", "Не выбрана fuzzy-переменная")
            return

        if not self.scene.validate_all():
            QMessageBox.warning(
                self,
                "Ошибка",
                "Нарушено условие A ≤ B ≤ C ≤ D"
            )
            return

        terms = self.repository.get_terms(self.fuzzy_variable_id)
        data = self.scene.get_functions_data()

        count = min(len(terms), len(data))

        for i in range(count):
            self.repository.save_membership_function(
                terms[i]["id"],
                data[i]["a"],
                data[i]["b"],
                data[i]["c"],
                data[i]["d"]
            )

        QMessageBox.information(self, "Успех", "Функции сохранены")