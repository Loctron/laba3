from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox


class ConditionRow(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.attribute_combo = QComboBox()
        self.operator_combo = QComboBox()
        self.value_combo = QComboBox()

        self.operator_combo.addItems(["=", "!=", ">", "<", ">=", "<="])

        layout.addWidget(self.attribute_combo)
        layout.addWidget(self.operator_combo)
        layout.addWidget(self.value_combo)

        self.setLayout(layout)

    def set_values(self, values):
        self.value_combo.clear()
        for v in values:
            self.value_combo.addItem(v["value"])