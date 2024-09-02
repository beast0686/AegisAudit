from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import pyqtSignal

class UserManagement(QWidget):
    user_logged_in = pyqtSignal()  # Signal to notify that a user has logged in

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

        self.login_button = QPushButton("Login as Selected User")
        self.login_button.clicked.connect(self.login_user)
        self.layout.addWidget(self.login_button)

    def add_user(self):
        self.users_table.setRowCount(self.users_table.rowCount() + 1)
        self.users_table.setItem(self.users_table.rowCount() - 1, 0, QTableWidgetItem("newuser"))
        self.users_table.setItem(self.users_table.rowCount() - 1, 1, QTableWidgetItem("Auditor"))
        self.users_table.setItem(self.users_table.rowCount() - 1, 2, QTableWidgetItem("Active"))
        QMessageBox.information(self, "User Added", "New user has been added.")

    def login_user(self):
        selected_row = self.users_table.currentRow()
        if selected_row != -1:
            QMessageBox.information(self, "User Logged In", f"Logged in as {self.users_table.item(selected_row, 0).text()}")
            self.user_logged_in.emit()  # Emit signal when user logs in
        else:
            QMessageBox.warning(self, "Login Failed", "Please select a user to log in.")
