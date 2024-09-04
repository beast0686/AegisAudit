from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import json


class AuditConfiguration(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Filter section
        self.filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Security", "Performance", "Compliance"])
        self.filter_combo.currentTextChanged.connect(self.filter_logs)
        self.filter_layout.addWidget(QLabel("Filter:"))
        self.filter_layout.addWidget(self.filter_combo)
        self.layout.addLayout(self.filter_layout)

        # Search section
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search audit logs...")
        self.search_input.textChanged.connect(self.search_logs)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_logs)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.layout.addLayout(self.search_layout)

        # Table for audit logs
        self.audit_log_table = QTableWidget()
        self.audit_log_table.setColumnCount(3)
        self.audit_log_table.setHorizontalHeaderLabels(["Audit Type", "Details", "Status"])
        self.audit_log_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.audit_log_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.layout.addWidget(self.audit_log_table)

        # Load tick and cross images
        self.tick_pixmap = QPixmap(r"..\images\Results\check.png")
        self.cross_pixmap = QPixmap(r"..\images\Results\cross.png")

        # Save and Load buttons
        self.save_config_button = QPushButton("Save Configuration")
        self.save_config_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_config_button)

        self.load_config_button = QPushButton("Load Configuration")
        self.load_config_button.clicked.connect(self.load_config)
        self.layout.addWidget(self.load_config_button)

        # Example audit logs
        self.audit_logs = [
            {"audit_type": "Security", "details": "Security check 1 completed.", "status": True},
            {"audit_type": "Performance", "details": "Performance check 1 completed.", "status": True},
            {"audit_type": "Compliance", "details": "Compliance check 1 not completed.", "status": False},
            {"audit_type": "Security", "details": "Security check 2 completed.", "status": True},
            {"audit_type": "Performance", "details": "Performance check 2 not completed.", "status": False},
        ]

        # Load logs into the table
        self.load_audit_logs()

    def load_audit_logs(self):
        self.audit_log_table.setRowCount(0)  # Clear existing logs
        for log in self.audit_logs:
            self.add_log_to_table(log)

    def add_log_to_table(self, log):
        row_position = self.audit_log_table.rowCount()
        self.audit_log_table.insertRow(row_position)
        self.audit_log_table.setItem(row_position, 0, QTableWidgetItem(log["audit_type"]))
        self.audit_log_table.setItem(row_position, 1, QTableWidgetItem(log["details"]))

        status_label = QLabel()
        if log["status"]:
            status_label.setPixmap(self.tick_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            status_label.setPixmap(self.cross_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audit_log_table.setCellWidget(row_position, 2, status_label)

    def save_config(self):
        config = {
            "audit_logs": self.audit_logs
        }
        with open("config.json", "w") as f:
            json.dump(config, f)
        QMessageBox.information(self, "Configuration Saved", "Audit logs have been saved.")

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                self.audit_logs = config.get("audit_logs", [])
                self.load_audit_logs()
        except FileNotFoundError:
            QMessageBox.warning(self, "Configuration Not Found", "No saved configuration found.")

    def search_logs(self):
        search_text = self.search_input.text().lower()
        for row in range(self.audit_log_table.rowCount()):
            match = False
            for column in range(self.audit_log_table.columnCount()):
                item = self.audit_log_table.item(row, column)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.audit_log_table.setRowHidden(row, not match)

    def filter_logs(self):
        selected_filter = self.filter_combo.currentText()
        for row in range(self.audit_log_table.rowCount()):
            item = self.audit_log_table.item(row, 0)  # Audit Type column
            if selected_filter == "All" or item.text() == selected_filter:
                self.audit_log_table.setRowHidden(row, False)
            else:
                self.audit_log_table.setRowHidden(row, True)
