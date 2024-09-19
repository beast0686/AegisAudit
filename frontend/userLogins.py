import Register_Login
from PyQt6.QtWidgets import QDialog, QFormLayout, QLabel, QDialogButtonBox, QWidget, QVBoxLayout, QGridLayout, QPushButton, QMessageBox, QLineEdit, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize
import sqlite3
import os

class UserManagement(QWidget):
    user_logged_in = pyqtSignal()  # Signal to notify that a user has logged in

    def __init__(self):
        super().__init__()

        # Set up main layout and grid layout for user profiles
        self.main_layout = QVBoxLayout(self)
        self.user_grid = QGridLayout()
        self.user_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the grid
        self.main_layout.addLayout(self.user_grid)

        # Create Database
        Register_Login.create_db()

        # Add users to the grid layout
        self.fill_grid_with_profiles()

        # Add User Button
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)
        self.add_user_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.add_user_button, alignment=Qt.AlignmentFlag.AlignCenter)

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
                # Update the grid with the new user
                self.fill_grid_with_profiles()
                QMessageBox.information(self, "User Added", "New user has been added successfully.")
            else:
                QMessageBox.warning(self, "Database Error", "Failed to add the user to the database.")

    def login_user(self, username):
        # Handle user login and emit signal
        QMessageBox.information(self, "User Logged In", f"Logged in as {username}")
        self.user_logged_in.emit()

    def fill_grid_with_profiles(self):
        # Clear the grid layout first
        for i in reversed(range(self.user_grid.count())):
            widget = self.user_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Get user data from the database
        accounts = self.get_users()

        # Populate the grid with profile pictures and usernames
        row, col = 0, 0
        for account in accounts:
            user_id, username = account

            # Create a button for the user profile with an icon (profile picture)
            user_button = QPushButton()
            user_button.setIcon(QIcon(self.get_profile_picture_path(user_id)))
            user_button.setIconSize(QSize(100, 100))  # Set icon size
            user_button.setFlat(True)  # Make the button flat (no border)
            user_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

            # Connect button click to login action
            user_button.clicked.connect(lambda _, u=username: self.login_user(u))

            # Create a label for the username
            username_label = QLabel(username)
            username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            username_label.setFont(QFont('Cascadia Code', 12))  # Set font for username

            # Add button and label to the grid layout
            self.user_grid.addWidget(user_button, row, col, alignment=Qt.AlignmentFlag.AlignCenter)
            self.user_grid.addWidget(username_label, row + 1, col, alignment=Qt.AlignmentFlag.AlignCenter)

            # Move to the next column and row
            col += 1
            if col >= 3:  # Limit to 3 profiles per row
                col = 0
                row += 2

    def get_profile_picture_path(self, user_id):
        # Get the profile picture path for the user, use a default if not found
        profile_pic_dir = "../profile_pictures/"
        profile_pic_path = os.path.join(profile_pic_dir, f"user_{user_id}.png")
        if not os.path.exists(profile_pic_path):
            profile_pic_path = "../profile_pictures/pfp.png"  # Default picture
        return profile_pic_path

    def get_users(self):
        # Retrieve user information from the database
        mydb = sqlite3.connect("../../AegisAudit/frontend/AegisAudit.db")
        cursor = mydb.cursor()
        cursor.execute('SELECT Admin_id, admin_name FROM Admin')
        rows = cursor.fetchall()
        mydb.close()
        return rows

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
