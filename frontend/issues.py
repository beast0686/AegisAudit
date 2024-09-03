from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QHeaderView


class IssueManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Issues Table
        self.issues_table = QTableWidget()
        self.issues_table.setRowCount(3)
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

        # Mark as Unresolved Button
        self.mark_unresolved_button = QPushButton("Mark as Unresolved")
        self.mark_unresolved_button.clicked.connect(self.mark_unresolved)
        self.layout.addWidget(self.mark_unresolved_button)

    def mark_resolved(self):
        selected_row = self.issues_table.currentRow()
        if selected_row != -1:
            # Set the status with tick image
            status_label = QLabel()
            pixmap = QPixmap(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\Issues\check.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            status_label.setPixmap(pixmap)
            status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image in the cell
            self.issues_table.setCellWidget(selected_row, 3, status_label)
            QMessageBox.information(self, "Issue Resolved", "Issue has been marked as resolved.")

    def mark_unresolved(self):
        selected_row = self.issues_table.currentRow()
        if selected_row != -1:
            # Set the status with cross image
            status_label = QLabel()
            pixmap = QPixmap(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\Issues\cross.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            status_label.setPixmap(pixmap)
            status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image in the cell
            self.issues_table.setCellWidget(selected_row, 3, status_label)
            QMessageBox.information(self, "Issue Unresolved", "Issue has been marked as unresolved.")
