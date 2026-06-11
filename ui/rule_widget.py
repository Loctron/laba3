from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QComboBox,
    QMessageBox
)

from database.rule_repository import RuleRepository
from database.attribute_repository import AttributeRepository
from ui.condition_row import ConditionRow


class RuleWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.project_id = None

        self.rule_repository = RuleRepository()
        self.attribute_repository = AttributeRepository()

        self.condition_rows = []

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Название правила"))

        self.rule_name = QLineEdit()
        layout.addWidget(self.rule_name)

        layout.addWidget(QLabel("УСЛОВИЯ"))

        self.conditions_layout = QVBoxLayout()
        layout.addLayout(self.conditions_layout)

        self.add_condition_btn = QPushButton(
            "Добавить условие"
        )

        layout.addWidget(self.add_condition_btn)

        layout.addWidget(QLabel("ТО"))

        self.then_attr = QComboBox()
        self.then_val = QComboBox()

        layout.addWidget(self.then_attr)
        layout.addWidget(self.then_val)

        layout.addWidget(QLabel("Объяснение"))

        self.explanation = QTextEdit()
        layout.addWidget(self.explanation)

        self.save_btn = QPushButton("Сохранить")
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.add_condition_btn.clicked.connect(
            self.add_condition
        )

        self.save_btn.clicked.connect(
            self.save_rule
        )

        self.then_attr.currentIndexChanged.connect(
            self.update_then_values
        )

    def set_project(self, project_id):
        self.project_id = project_id

        if not project_id:
            return

        self.load_attributes()

    def load_attributes(self):

        self.then_attr.clear()

        attrs = self.attribute_repository.get_all_attributes(
            self.project_id
        )

        for attr in attrs:

            self.then_attr.addItem(
                attr["name"],
                attr["id"]
            )

        self.update_then_values()

    def update_then_values(self):

        self.then_val.clear()

        attribute_id = self.then_attr.currentData()

        if attribute_id is None:
            return

        values = (
            self.attribute_repository
            .get_attribute_values(attribute_id)
        )

        for value in values:

            self.then_val.addItem(
                value["value"]
            )

    def add_condition(self):

        row = ConditionRow()

        attrs = self.attribute_repository.get_all_attributes(
            self.project_id
        )

        for attr in attrs:

            row.attribute_combo.addItem(
                attr["name"],
                attr["id"]
            )

        row.attribute_combo.currentIndexChanged.connect(
            lambda _, r=row:
            self.update_condition_values(r)
        )

        self.update_condition_values(row)

        self.condition_rows.append(row)

        self.conditions_layout.addWidget(row)

    def update_condition_values(self, row):

        row.value_combo.clear()

        attribute_id = row.attribute_combo.currentData()

        if attribute_id is None:
            return

        values = (
            self.attribute_repository
            .get_attribute_values(attribute_id)
        )

        for value in values:

            row.value_combo.addItem(
                value["value"]
            )

    def save_rule(self):

        if not self.project_id:
            QMessageBox.warning(self, "Ошибка", "Не выбран проект")
            return

        name = self.rule_name.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите имя правила")
            return

        rule_id = self.rule_repository.add_rule(self.project_id, name)

        # IF
        for row in self.condition_rows:

            attr_id = row.attribute_combo.currentData()
            val = row.value_combo.currentText()

            if attr_id and val:
                self.rule_repository.add_condition(
                    rule_id,
                    attr_id,
                    val,
                    "IF"
                )

        # THEN
        self.rule_repository.add_condition(
            rule_id,
            self.then_attr.currentData(),
            self.then_val.currentText(),
            "THEN"
        )

        # объяснение
        self.rule_repository.add_explanation(
            rule_id,
            self.explanation.toPlainText()
        )

        QMessageBox.information(self, "Успех", "Правило сохранено")