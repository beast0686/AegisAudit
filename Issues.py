from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox

class IssueManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.issues_table = QTableWidget()
        self.issues_table.setRowCount(0)
        self.issues_table.setColumnCount(4)
        self.issues_table.setHorizontalHeaderLabels(['Issue', 'Severity', 'Description', 'Status'])
        self.layout.addWidget(self.issues_table)

        self.mark_resolved_button = QPushButton("Mark as Resolved")
        self.mark_resolved_button.clicked.connect(self.mark_resolved)
        self.layout.addWidget(self.mark_resolved_button)

    def mark_resolved(self):
        selected_row = self.issues_table.currentRow()
        if selected_row != -1:
            self.issues_table.setItem(selected_row, 3, QTableWidgetItem("Resolved"))
            QMessageBox.information(self, "Issue Resolved", "Issue has been marked as resolved.")
