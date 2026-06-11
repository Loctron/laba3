from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem,
    QTabWidget, QMessageBox
)

from database.fuzzy_repository import FuzzyRepository
from database.project_repository import ProjectRepository
from database.attribute_repository import AttributeRepository
from database.rule_repository import RuleRepository

from ui.project_widget import ProjectWidget
from ui.attribute_widget import AttributeWidget
from ui.rule_widget import RuleWidget
from ui.explanation_widget import ExplanationWidget
from ui.membership_editor_widget import MembershipEditorWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Knowledge Base IDE")
        self.resize(1300, 750)

        self.project_repository = ProjectRepository()
        self.attribute_repository = AttributeRepository()
        self.rule_repository = RuleRepository()

        self.current_project_id = None

        self.create_menu()
        self.create_ui()
        self.load_projects()

    # ================= Меню =================
    def create_menu(self):

        menu = self.menuBar()

        project_menu = menu.addMenu("Проект")
        attribute_menu = menu.addMenu("Атрибуты")
        rule_menu = menu.addMenu("Правила")
        explanation_menu = menu.addMenu("Объяснения")
        fuzzy_menu = menu.addMenu("Нечёткие множества")

        project_menu.addAction("Открыть проекты", self.open_project_editor)
        attribute_menu.addAction("Открыть атрибуты", self.open_attribute_editor)
        rule_menu.addAction("Открыть правила", self.open_rule_editor)
        explanation_menu.addAction("Открыть объяснения", self.open_explanation_editor)
        fuzzy_menu.addAction("Редактор функций принадлежности", self.open_fuzzy_editor)

    # ================= UI =================
    def create_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        central.setLayout(layout)

        # Левая панель
        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel("Проекты")
        self.project_tree.itemClicked.connect(self.on_project_selected)

        # Центр
        self.tabs = QTabWidget()

        layout.addWidget(self.project_tree, 1)
        layout.addWidget(self.tabs, 4)

    # ================= Проекты =================
    def load_projects(self):

        self.project_tree.clear()

        projects = self.project_repository.get_all_projects()

        nodes = {}

        for p in projects:
            node = QTreeWidgetItem([p["name"]])
            node.setData(0, 1, p["id"])
            nodes[p["id"]] = node

        for p in projects:

            node = nodes[p["id"]]

            if p["parent_id"] and p["parent_id"] in nodes:
                nodes[p["parent_id"]].addChild(node)
            else:
                self.project_tree.addTopLevelItem(node)

    def on_project_selected(self, item):

        self.current_project_id = item.data(0, 1)

    # ================= Открытие редактора =================
    def open_project_editor(self):
        widget = ProjectWidget(
            refresh_callback=self.load_projects
        )

        self.tabs.addTab(widget, "Проекты")

    def open_rule_editor(self):
        w = RuleWidget()
        w.set_project(self.current_project_id)
        self.tabs.addTab(w, "Rules")


    def open_attribute_editor(self):
        w = AttributeWidget()
        w.project_id = self.current_project_id
        self.tabs.addTab(w, "Attributes")

    def open_explanation_editor(self):

        widget = ExplanationWidget()

        if self.current_project_id:
            widget.load(self.current_project_id)

        self.tabs.addTab(widget, "Объяснения")

    def open_fuzzy_editor(self):

        if not self.current_project_id:
            return

        widget = MembershipEditorWidget()

        attrs = self.attribute_repository.get_all_attributes(
            self.current_project_id
        )

        repo = FuzzyRepository()

        for attr in attrs:

            fuzzy_var = (
                repo.get_fuzzy_variable_by_attribute(
                    attr["id"]
                )
            )

            if fuzzy_var:

                widget.load_variable(
                    fuzzy_var["id"]
                )

                self.tabs.addTab(
                    widget,
                    "Нечёткие множества"
                )

                return

        QMessageBox.warning(
            self,
            "Ошибка",
            "Нет нечётких атрибутов"
        )