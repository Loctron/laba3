from PyQt5.QtWidgets import (
    QInputDialog,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QMessageBox
)

from database.project_repository import ProjectRepository


class ProjectWidget(QWidget):

    def __init__(self, refresh_callback=None):
        super().__init__()

        self.repository = ProjectRepository()
        self.current_project_id = None

        self.refresh_callback = refresh_callback
        self.create_ui()
        self.load_projects()

    def create_ui(self):

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Название проекта")
        )

        self.name_edit = QLineEdit()

        layout.addWidget(
            self.name_edit
        )

        layout.addWidget(
            QLabel("Родительский проект")
        )

        self.parent_combo = QComboBox()

        layout.addWidget(
            self.parent_combo
        )

        buttons = QHBoxLayout()

        self.add_button = QPushButton(
            "Создать"
        )

        self.rename_button = QPushButton(
            "Переименовать"
        )

        self.delete_button = QPushButton(
            "Удалить"
        )

        self.copy_button = QPushButton("Копировать")
        self.paste_button = QPushButton("Вставить")

        buttons.addWidget(self.add_button)
        buttons.addWidget(self.rename_button)
        buttons.addWidget(self.delete_button)
        buttons.addWidget(self.copy_button)
        buttons.addWidget(self.paste_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.add_button.clicked.connect(
            self.add_project
        )

        self.rename_button.clicked.connect(
            self.rename_project
        )

        self.delete_button.clicked.connect(
            self.delete_project
        )

        self.copy_button.clicked.connect(
            self.copy_project
        )

        self.paste_button.clicked.connect(
            self.paste_project
        )

        self.parent_combo.currentIndexChanged.connect(
            self.select_project
        )

        self.copied_project_id = None

    def load_projects(self):

        self.parent_combo.clear()

        self.parent_combo.addItem(
            "Нет",
            None
        )

        projects = (
            self.repository
            .get_all_projects()
        )

        for project in projects:

            self.parent_combo.addItem(
                project["name"],
                project["id"]
            )

    def select_project(self):

        self.current_project_id = (
            self.parent_combo.currentData()
        )

    def add_project(self):

        name = self.name_edit.text().strip()

        if not name:
            return

        parent_id = self.parent_combo.currentData()

        self.repository.add_project(name, parent_id)

        QMessageBox.information(
            self,
            "Успех",
            "Проект создан"
        )

        self.name_edit.clear()

        self.load_projects()

        # 🔥 ВАЖНО
        if self.refresh_callback:
            self.refresh_callback()

    def rename_project(self):

        if self.current_project_id is None:
            return

        new_name = self.name_edit.text().strip()

        if not new_name:
            return

        self.repository.rename_project(
            self.current_project_id,
            new_name
        )

        QMessageBox.information(
            self,
            "Успех",
            "Проект переименован"
        )

        self.load_projects()

    def delete_project(self):

        if self.current_project_id is None:
            return

        self.repository.delete_project(
            self.current_project_id
        )

        QMessageBox.information(
            self,
            "Успех",
            "Проект удалён"
        )

        self.load_projects()

    def copy_project(self):

        project_id, ok = QInputDialog.getInt(
            self,
            "Копирование",
            "ID проекта"
        )

        if ok:
            self.copied_project_id = project_id

    def paste_project(self):

        if self.copied_project_id is None:
            return

        name, ok = QInputDialog.getText(
            self,
            "Вставка",
            "Имя нового проекта"
        )

        if ok and name:

            self.repository.copy_project(
                self.copied_project_id,
                name
            )

            self.load_projects()

            if self.refresh_callback:
                self.refresh_callback()