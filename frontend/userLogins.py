import os
import sqlite3
import Register_Login
from PyQt6.QtWidgets import QDialog, QFormLayout, QLabel, QDialogButtonBox, QWidget, QVBoxLayout, QGridLayout, \
    QPushButton, QMessageBox, QLineEdit, QSizePolicy, QFileDialog
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QPixmap, QDragEnterEvent, QDropEvent

from os.path import join, dirname, abspath
db_path = join(dirname(dirname(abspath(__file__))), 'AegisAudit.db')

class UserManagement(QWidget):
    user_logged_in = pyqtSignal()  # Signal to notify that a user has logged in

    def __init__(self):
        super().__init__()

        # Create Database and admin
        Register_Login.create_db()

        # Set up main layout and grid layout for user profiles
        self.main_layout = QVBoxLayout(self)
        self.user_grid = QGridLayout()
        self.user_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the grid
        self.main_layout.addLayout(self.user_grid)

        # Add users to the grid layout
        self.fill_grid_with_profiles()

        # Add User Button
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)
        self.add_user_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.add_user_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def add_user(self):
        dialog = AddUserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, password, profile_pic_path = dialog.get_data()
            # Validate input
            if not username or not password:
                QMessageBox.warning(self, "Input Error", "Username and password are required.")
                return

            # Call the create_user method to add the user to the database
            user_created = Register_Login.create_user(username, password, profile_pic_path)

            if user_created:
                # Update the grid with the new user
                self.fill_grid_with_profiles()
                QMessageBox.information(self, "User Added", "New user has been added successfully.")
            else:
                QMessageBox.warning(self, "Database Error", "Failed to add the user to the database.")

    def login_user(self, username):
        # Handle user login and emit signal
        dialog = LoginUserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            password = dialog.get_data()
            if not password:
                QMessageBox.warning(self, "Input Error", "Password is required.")
                return

            user_loggedin = Register_Login.login_user(username, password)
            if user_loggedin:
                QMessageBox.information(self, "User Logged In", f"Logged in as {username}")
                self.user_logged_in.emit()
            else:
                QMessageBox.warning(self, "Failed to login", "Invalid password.")

# WorkSP: M5FU8GRS
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
            user_id, username, profile_picture = account

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
        mydb = sqlite3.connect(db_path)
        cursor = mydb.cursor()

        # Ensure that user_id is passed as a tuple
        cursor.execute('SELECT profile_picture FROM accounts WHERE id = ?', (user_id,))
        profile_pic_record = cursor.fetchone()  # Fetch the result

        # Check if the user has a custom profile picture
        if profile_pic_record and profile_pic_record[0]:
            profile_pic_path = profile_pic_record[0]
        else:
            # Set default profile picture path
            profile_pic_path = "../profile_pictures/user_icon.png"

        return profile_pic_path

    def get_users(self):
        # Retrieve user information from the database
        mydb = sqlite3.connect(db_path)
        cursor = mydb.cursor()
        cursor.execute('SELECT id, name, profile_picture FROM accounts')
        rows = cursor.fetchall()
        mydb.close()
        return rows

class LoginUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login User")

        # Create layout and form fields
        layout = QFormLayout(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(QLabel("Password:"), self.password_input)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                        self)
        layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_data(self):
        # Return the username and password entered by the user
        return self.password_input.text()

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        self.image_file_path = None  # Attribute to store the selected image path

        # Create layout and form fields
        layout = QFormLayout(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(QLabel("Username:"), self.username_input)
        layout.addRow(QLabel("Password:"), self.password_input)

        # Profile picture drag-and-drop area
        self.picture_label = ImageLabel(self)
        layout.addRow(QLabel("Profile Picture:"), self.picture_label)

        # Browse button to allow file selection
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.on_ok_clicked)
        self.buttons.rejected.connect(self.reject)

    def browse_file(self):
        """Open a file dialog to browse for a file and return the file path."""
        file_dialog = QFileDialog(self)

        file_dialog.setWindowTitle("Select an Image")
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():  # If the user selects a file
            selected_file = file_dialog.selectedFiles()[0]  # Get the selected file
            self.image_file_path = selected_file  # Store the file path in the class attribute
            print(f"Selected file: {self.image_file_path}")
        else:
            print("No file selected")

    def on_ok_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Get the image file path from drag-and-drop or browse
        self.image_file_path = self.picture_label.save_image(r"..\\user_profile_pictures\\") if self.picture_label.image_path else self.image_file_path

        if not self.image_file_path:
            self.image_file_path = r"..\profile_pictures\user_icon.png"
        self.accept()

    def get_data(self):
        # Return the username and password entered by the user
        return self.username_input.text(), self.password_input.text(), self.image_file_path


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 150)
        self.setStyleSheet("border: 1px solid black;")
        self.setText("Drag and Drop Image Here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAcceptDrops(True)
        self.image = None  # Store the pixmap
        self.image_path = None  # To store the file path

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and self.is_image_file(event.mimeData().urls()[0].toLocalFile()):
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if self.is_image_file(file_path):
                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
                self.setPixmap(pixmap)
                self.setText("")  # Clear the "Drag and Drop" text
                self.image = pixmap  # Store the pixmap
                self.image_path = file_path  # Store the image path

    def is_image_file(self, file_path: str) -> bool:
        return file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))

    def save_image(self, destination_folder):
        """Save the image to the destination folder using os module."""
        if self.image_path:
            # Get the filename from the original file path
            file_name = os.path.basename(self.image_path)
            # Destination path
            destination_path = os.path.join(destination_folder, file_name)
            # Copy the file using os module
            with open(self.image_path, 'rb') as src_file:
                with open(destination_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())
            return destination_path
        return None
