from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QAbstractItemView, QHeaderView, QTabWidget, \
    QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create the tab widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Create Summary Tab
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout()
        self.summary_tab.setLayout(self.summary_layout)

        self.summary_label = QLabel("Summary of Audit Log Checks")
        self.summary_layout.addWidget(self.summary_label)

        # Table for summary details
        self.summary_table = QTableWidget()
        self.summary_table.setRowCount(3)  # Example: 3 audit checks
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(['Check Name', 'Description'])
        self.summary_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Adding example audit check details
        self.summary_table.setItem(0, 0, QTableWidgetItem("Check for Config Files"))
        self.summary_table.setItem(0, 1, QTableWidgetItem("Verifies that all configuration files are in place."))
        self.summary_table.setItem(1, 0, QTableWidgetItem("Security Policies Compliance"))
        self.summary_table.setItem(1, 1, QTableWidgetItem("Ensures that all security policies are being followed."))
        self.summary_table.setItem(2, 0, QTableWidgetItem("Database Integrity"))
        self.summary_table.setItem(2, 1, QTableWidgetItem("Checks if the database maintains referential integrity."))

        self.summary_layout.addWidget(self.summary_table)

        # Add summary tab to the tab widget
        self.tabs.addTab(self.summary_tab, "Summary")

        # Create History Tab
        self.history_tab = QWidget()
        self.history_layout = QVBoxLayout()
        self.history_tab.setLayout(self.history_layout)

        self.audit_history_label = QLabel("Audit History")
        self.history_layout.addWidget(self.audit_history_label)

        # Table for audit history details
        self.audit_history_table = QTableWidget()
        self.audit_history_table.setRowCount(3)  # Example: 3 history entries
        self.audit_history_table.setColumnCount(3)
        self.audit_history_table.setHorizontalHeaderLabels(['Audit Name', 'Status', 'Date'])
        self.audit_history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.audit_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Load tick and cross images
        self.tick_pixmap = QPixmap(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\Issues\check.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.cross_pixmap = QPixmap(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\Issues\cross.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Adding example audit history details with images for status
        self.add_audit_history_row(0, "Initial Configuration Audit", True, "2024-09-01")
        self.add_audit_history_row(1, "Security Policy Audit", False, "2024-09-02")
        self.add_audit_history_row(2, "Database Integrity Check", True, "2024-09-03")

        self.history_layout.addWidget(self.audit_history_table)

        # Add history tab to the tab widget
        self.tabs.addTab(self.history_tab, "History")

    def add_audit_history_row(self, row, audit_name, completed, date):
        self.audit_history_table.setItem(row, 0, QTableWidgetItem(audit_name))
        self.audit_history_table.setItem(row, 2, QTableWidgetItem(date))

        status_label = QLabel()
        if completed:
            status_label.setPixmap(self.tick_pixmap)
        else:
            status_label.setPixmap(self.cross_pixmap)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image in the cell
        self.audit_history_table.setCellWidget(row, 1, status_label)
