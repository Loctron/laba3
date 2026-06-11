from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,
    QListWidget, QTextEdit, QPushButton
)

from database.rule_repository import RuleRepository


class ExplanationWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.repo = RuleRepository()
        self.project_id = None
        self.rules_map = []

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout()

        self.rule_list = QListWidget()
        self.text = QTextEdit()
        self.save_btn = QPushButton("Сохранить")

        layout.addWidget(self.rule_list)
        layout.addWidget(self.text)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.rule_list.currentRowChanged.connect(self.load_explanation)
        self.save_btn.clicked.connect(self.save)

    def load(self, project_id):
        self.project_id = project_id

        self.rule_list.clear()
        self.rules_map = self.repo.get_rules(project_id)

        for r in self.rules_map:
            self.rule_list.addItem(r["name"])

    def load_explanation(self, index):
        if index < 0:
            return

        rule = self.rules_map[index]
        exp = self.repo.get_explanation(rule["id"])

        if exp:
            self.text.setPlainText(exp["explanation_text"])
        else:
            self.text.clear()

    def save(self):
        idx = self.rule_list.currentRow()
        if idx < 0:
            return

        rule_id = self.rules_map[idx]["id"]

        self.repo.add_explanation(
            rule_id,
            self.text.toPlainText()
        )