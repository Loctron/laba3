from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QInputDialog,
    QMessageBox
)

from database.attribute_repository import AttributeRepository
from database.fuzzy_repository import FuzzyRepository


class AttributeWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.repository = AttributeRepository()
        self.fuzzy_repository = FuzzyRepository()

        self.project_id = None

        self.copied_attribute_id = None

        self.current_attribute_id = None

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Атрибуты проекта"))

        # выбор атрибута
        self.attribute_combo = QComboBox()
        layout.addWidget(self.attribute_combo)

        self.load_attributes()

        self.attribute_combo.currentIndexChanged.connect(
            self.select_attribute
        )

        layout.addWidget(QLabel("Название атрибута"))

        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("Тип значения"))

        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "NUMERIC",
            "STRING",
            "BOOLEAN",
            "DATE",
            "FUZZY"
        ])
        layout.addWidget(self.type_combo)

        layout.addWidget(QLabel("Тип нечёткости"))

        self.fuzzy_combo = QComboBox()
        self.fuzzy_combo.addItems([
            "",
            "FUZZY_NUMBER",
            "FUZZY_VARIABLE",
            "LINGUISTIC_VARIABLE"
        ])
        layout.addWidget(self.fuzzy_combo)

        layout.addWidget(QLabel("Терм-множество"))

        self.term_list = QListWidget()
        layout.addWidget(self.term_list)

        self.add_term_button = QPushButton("Добавить терм")
        self.remove_term_button = QPushButton("Удалить терм")

        layout.addWidget(self.add_term_button)
        layout.addWidget(self.remove_term_button)

        buttons = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.delete_button = QPushButton("Удалить")
        self.copy_button = QPushButton("Копировать")
        self.paste_button = QPushButton("Вставить")
        self.rename_button = QPushButton("Переименовать")

        buttons.addWidget(self.add_button)
        buttons.addWidget(self.delete_button)
        buttons.addWidget(self.copy_button)
        buttons.addWidget(self.paste_button)
        buttons.addWidget(self.rename_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

        # сигналы
        self.add_button.clicked.connect(self.add_attribute)
        self.delete_button.clicked.connect(self.delete_attribute)
        self.copy_button.clicked.connect(self.copy_attribute)
        self.paste_button.clicked.connect(self.paste_attribute)
        self.rename_button.clicked.connect(self.rename_attribute)

        self.add_term_button.clicked.connect(self.add_term)
        self.remove_term_button.clicked.connect(self.remove_term)

    # =========================
    # АТРИБУТЫ
    # =========================

    def add_attribute(self):

        if self.project_id is None:
            return

        self.repository.add_attribute(
            self.project_id,
            self.name_edit.text(),
            self.type_combo.currentText(),
            self.fuzzy_combo.currentText()
        )

        attrs = self.repository.get_all_attributes(
            self.project_id
        )

        attr_id = attrs[-1]["id"]

        if self.type_combo.currentText() == "FUZZY":

            self.fuzzy_repository.create_fuzzy_variable(
                attr_id,
                self.name_edit.text(),
                0,
                100,
                1
            )

        QMessageBox.information(
            self,
            "Успех",
            "Атрибут создан"
        )

        self.load_attributes()

    def delete_attribute(self):

        attribute_id, ok = QInputDialog.getInt(
            self, "Удаление", "ID атрибута"
        )

        if ok:
            self.repository.delete_attribute(attribute_id)
            QMessageBox.information(self, "Успех", "Атрибут удалён")
            self.load_attributes()

    def rename_attribute(self):

        attribute_id, ok = QInputDialog.getInt(
            self, "Переименование", "ID атрибута"
        )

        if not ok:
            return

        new_name, ok = QInputDialog.getText(
            self, "Переименование", "Новое имя"
        )

        if ok:
            self.repository.rename_attribute(attribute_id, new_name)
            QMessageBox.information(self, "Успех", "Атрибут переименован")
            self.load_attributes()

    def copy_attribute(self):

        attribute_id, ok = QInputDialog.getInt(
            self, "Копирование", "ID атрибута"
        )

        if ok:
            self.copied_attribute_id = attribute_id

    def paste_attribute(self):

        if self.copied_attribute_id is None or self.project_id is None:
            return

        self.repository.copy_attribute(
            self.copied_attribute_id,
            self.project_id
        )

        QMessageBox.information(self, "Успех", "Атрибут вставлен")
        self.load_attributes()

    # =========================
    # ВЫБОР АТРИБУТА
    # =========================

    def load_attributes(self):

        self.attribute_combo.clear()

        if self.project_id is None:
            return

        attrs = self.repository.get_all_attributes(self.project_id)

        for a in attrs:
            self.attribute_combo.addItem(a["name"], a["id"])

        if attrs:
            self.current_attribute_id = attrs[0]["id"]

    def select_attribute(self):

        self.current_attribute_id = self.attribute_combo.currentData()

        self.load_terms()

    # =========================
    # ТЕРМЫ
    # =========================

    def add_term(self):

        text, ok = QInputDialog.getText(
            self,
            "Терм",
            "Название терма"
        )

        if not (ok and text):
            return

        if self.current_attribute_id is None:
            return

        self.repository.add_attribute_value(
            self.current_attribute_id,
            text
        )

        attr = self.repository.get_attribute(
            self.current_attribute_id
        )

        if attr["value_type"] == "FUZZY":

            fuzzy_var = (
                self.fuzzy_repository
                .get_fuzzy_variable_by_attribute(
                    self.current_attribute_id
                )
            )

            if fuzzy_var:

                self.fuzzy_repository.add_term(
                    fuzzy_var["id"],
                    text
                )

        self.load_terms()

    def remove_term(self):

        row = self.term_list.currentRow()

        if row >= 0:
            self.term_list.takeItem(row)

    def load_terms(self):

        self.term_list.clear()

        if self.current_attribute_id is None:
            return

        values = self.repository.get_attribute_values(
            self.current_attribute_id
        )

        for v in values:
            self.term_list.addItem(v["value"])