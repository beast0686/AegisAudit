from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton, QMessageBox
import json

class AuditConfiguration(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.audit_type_combo = QComboBox()
        self.audit_type_combo.addItems(["Security", "Performance", "Compliance"])
        self.layout.addWidget(self.audit_type_combo)

        self.custom_params_label = QLabel("Custom Parameters:")
        self.layout.addWidget(self.custom_params_label)

        self.custom_params_input = QLineEdit()
        self.layout.addWidget(self.custom_params_input)

        self.save_config_button = QPushButton("Save Configuration")
        self.save_config_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_config_button)

        self.load_config_button = QPushButton("Load Configuration")
        self.load_config_button.clicked.connect(self.load_config)
        self.layout.addWidget(self.load_config_button)

    def save_config(self):
        config = {
            "audit_type": self.audit_type_combo.currentText(),
            "custom_params": self.custom_params_input.text()
        }
        with open("config.json", "w") as f:
            json.dump(config, f)
        QMessageBox.information(self, "Configuration Saved", "Audit configuration has been saved.")

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                self.audit_type_combo.setCurrentText(config["audit_type"])
                self.custom_params_input.setText(config["custom_params"])
        except FileNotFoundError:
            QMessageBox.warning(self, "Configuration Not Found", "No saved configuration found.")
