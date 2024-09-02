from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox

class UserManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.users_table = QTableWidget()
        self.users_table.setRowCount(0)
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(['Username', 'Role', 'Status'])
        self.layout.addWidget(self.users_table)

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)
        self.layout.addWidget(self.add_user_button)

    def add_user(self):
        self.users_table.setRowCount(self.users_table.rowCount() + 1)
        self.users_table.setItem(self.users_table.rowCount() - 1, 0, QTableWidgetItem("newuser"))
        self.users_table.setItem(self.users_table.rowCount() - 1, 1, QTableWidgetItem("Auditor"))
        self.users_table.setItem(self.users_table.rowCount() - 1, 2, QTableWidgetItem("Active"))
        QMessageBox.information(self, "User Added", "New user has been added.")
