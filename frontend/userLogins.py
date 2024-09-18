import Register_Login
from PyQt6.QtWidgets import QDialog, QFormLayout, QLabel, QDialogButtonBox, QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox, QHeaderView, QInputDialog, QLineEdit
from PyQt6.QtCore import pyqtSignal
import sqlite3

class UserManagement(QWidget):
    user_logged_in = pyqtSignal()  # Signal to notify that a user has logged in

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create Database
        Register_Login.create_db()

        # Users Table
        self.num_of_rows = self.calculate_rows()
        self.users_table = QTableWidget()
        self.users_table.setRowCount(self.num_of_rows)
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(['Username', 'Role', 'Status'])
        self.fill_rows()

        # Adjusting column widths to fit the window size
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Username column
        self.users_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Role column
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Status column

        # Add the table to the layout
        self.layout.addWidget(self.users_table)

        # Add User Button
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)
        self.layout.addWidget(self.add_user_button)

        # Login Button
        self.login_button = QPushButton("Login as Selected User")
        self.login_button.clicked.connect(self.login_user)
        self.layout.addWidget(self.login_button)

    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, password = dialog.get_data()

            # Validate input
            if not username or not password:
                QMessageBox.warning(self, "Input Error", "Username and password are required.")
                return

            # Call the create_user method to add the user to the database
            user_created = Register_Login.create_user(username, password)
            if user_created:
                self.users_table.setRowCount(self.users_table.rowCount() + 1)
                self.users_table.setItem(self.users_table.rowCount() - 1, 0, QTableWidgetItem(username))
                self.users_table.setItem(self.users_table.rowCount() - 1, 1, QTableWidgetItem("Auditor"))
                self.users_table.setItem(self.users_table.rowCount() - 1, 2, QTableWidgetItem("Active"))
                QMessageBox.information(self, "User Added", "New user has been added successfully.")
            else:
                QMessageBox.warning(self, "Database Error", "Failed to add the user to the database.")

    def login_user(self):
        selected_row = self.users_table.currentRow()
        if selected_row != -1:
            QMessageBox.information(self, "User Logged In", f"Logged in as {self.users_table.item(selected_row, 0).text()}")
            self.user_logged_in.emit()  # Emit signal when user logs in
        else:
            QMessageBox.warning(self, "Login Failed", "Please select a user to log in.")

    def calculate_rows(self):
        mydb = sqlite3.connect("../../AegisAudit/frontend/AegisAudit.db")
        cursor = mydb.cursor()
        cursor.execute('SELECT COUNT(Admin_id) FROM Admin')
        row_count = cursor.fetchone()[0]
        mydb.close()
        return row_count

    def get_users(self):
        mydb = sqlite3.connect("../../AegisAudit/frontend/AegisAudit.db")
        cursor = mydb.cursor()
        cursor.execute('SELECT Admin_id, admin_name FROM Admin')
        rows = []
        for i in range(self.num_of_rows):
            row = cursor.fetchone()
            rows.append(row)
        mydb.close()
        return rows

    def fill_rows(self):
        accounts = self.get_users()
        for i in range(self.num_of_rows):
            id, username = accounts[i][0], accounts[i][1]
            self.users_table.setItem(i, 0, QTableWidgetItem(username))
            self.users_table.setItem(i, 1, QTableWidgetItem("Admin"))
            self.users_table.setItem(i, 2, QTableWidgetItem("Active"))
class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        # Create layout and form fields
        layout = QFormLayout(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(QLabel("Username:"), self.username_input)
        layout.addRow(QLabel("Password:"), self.password_input)
        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_data(self):
        # Return the username and password entered by the user
        return self.username_input.text(), self.password_input.text()