from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView  # Import QHeaderView for ResizeMode


class IssueManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Issues Table
        self.issues_table = QTableWidget()
        self.issues_table.setRowCount(0)
        self.issues_table.setColumnCount(4)
        self.issues_table.setHorizontalHeaderLabels(['Issue', 'Severity', 'Description', 'Status'])

        # Adjusting column widths to fit the window size
        self.issues_table.horizontalHeader().setStretchLastSection(True)
        self.issues_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Issue column
        self.issues_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Severity column
        self.issues_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Description column
        self.issues_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Status column

        # Add the table to the layout
        self.layout.addWidget(self.issues_table)

        # Mark as Resolved Button
        self.mark_resolved_button = QPushButton("Mark as Resolved")
        self.mark_resolved_button.clicked.connect(self.mark_resolved)
        self.layout.addWidget(self.mark_resolved_button)

    def mark_resolved(self):
        selected_row = self.issues_table.currentRow()
        if selected_row != -1:
            item = QTableWidgetItem("Resolved")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.issues_table.setItem(selected_row, 3, item)
            QMessageBox.information(self, "Issue Resolved", "Issue has been marked as resolved.")
