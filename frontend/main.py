import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QListWidget, QStackedWidget, QListWidgetItem
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
import os

# Direct imports since all files are in the same directory
from userLogins import UserManagement
from dashboard import Dashboard
from configuration import AuditConfiguration
from executionControl import ExecutionControl
from result import ResultsDisplay
from issues import IssueManagement


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up splitter for left and right window areas
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        # Create list widget for tab navigation (left window)
        self.tab_list = QListWidget()

        # Set large icon size for the tabs
        self.tab_list.setIconSize(QSize(48, 48))

        # Apply custom styling: remove black background and set text color to black
        self.tab_list.setStyleSheet("""
            QListWidget {
                font-size: 20px;  /* Larger font size */
                color: black;  /* Set text color to black */
            }
            QListWidget::item {
                padding: 10px;  /* Add space between items */
                margin-bottom: 10px;  /* Additional space at the bottom of each item */
            }
            QListWidget::item:selected {
                background-color: lightgray;  /* Light gray when selected */
                color: black;
            }
        """)

        # Align text properly by adding enough space after the icon
        self.tab_list.setUniformItemSizes(True)

        # Add tabs with icons
        self.add_tab("Profile", "../icons/profile.png", 0)
        self.add_tab("Dashboard", "../icons/dashboard.png", 1)
        self.add_tab("Audit Configuration", "../icons/configuration.png", 2)
        self.add_tab("Execution Control", "../icons/execution.png", 3)
        self.add_tab("Results Display", "../icons/results.png", 4)
        self.add_tab("Issue Management", "../icons/issues.png", 5)

        # Reduce the default width of the left panel (tab list)
        self.tab_list.setFixedWidth(250)

        # Create stacked widget to display the selected tab's content (right window)
        self.tab_content = QStackedWidget()

        # Set font size and font family for the right panel content
        self.tab_content.setStyleSheet("""
            QWidget {
                font-size: 16px;  /* Set text size to 16px */
                font-family: 'Palatino Linotype';  /* Set font to Palatino Linotype */
                color: black;  /* Set text color to black */
            }
        """)

        # Add the list and the tab content area to the splitter
        self.splitter.addWidget(self.tab_list)
        self.splitter.addWidget(self.tab_content)

        # Control the stretch factor to make the right side expand more
        self.splitter.setStretchFactor(0, 0)  # Left widget (tab list)
        self.splitter.setStretchFactor(1, 1)  # Right widget (content)

        # Create the tabs and add them to the stacked widget
        self.user_management_tab = UserManagement()
        self.tab_content.addWidget(self.user_management_tab)

        self.dashboard_tab = Dashboard()
        self.tab_content.addWidget(self.dashboard_tab)

        self.audit_config_tab = AuditConfiguration()
        self.tab_content.addWidget(self.audit_config_tab)

        self.execution_control_tab = ExecutionControl()
        self.tab_content.addWidget(self.execution_control_tab)

        self.results_display_tab = ResultsDisplay()
        self.tab_content.addWidget(self.results_display_tab)

        self.issue_management_tab = IssueManagement()
        self.tab_content.addWidget(self.issue_management_tab)

        # Disable all tabs except User Management by default
        self.enable_tabs(False)

        # Connect user management login signal
        self.user_management_tab.user_logged_in.connect(self.on_user_logged_in)

        # Connect the list widget to change the tab content when clicked
        self.tab_list.currentRowChanged.connect(self.switch_tab)

        # Set default selection to the User Management tab
        self.tab_list.setCurrentRow(0)

    def add_tab(self, name, icon_path, index):
        """Add a tab with an icon and name to the QListWidget"""
        item = QListWidgetItem(QIcon(icon_path), name)
        # Set alignment to make sure text starts after the icon at the same point
        item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.tab_list.addItem(item)

    def enable_tabs(self, enable):
        # Enable or disable all tabs except User Management
        for i in range(1, self.tab_list.count()):
            self.tab_list.item(i).setFlags(
                self.tab_list.item(i).flags() | (Qt.ItemFlag.ItemIsEnabled if enable else Qt.ItemFlag.ItemIsSelectable)
            )

    def on_user_logged_in(self):
        # Enable other tabs when a user is logged in
        self.enable_tabs(True)

    def switch_tab(self, index):
        # Switch to the corresponding tab content based on the index
        self.tab_content.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Ageis Audit")

    # Ensure the correct path for the logo icon
    logo_path = os.path.abspath("../icons/logo.png")  # Convert to absolute path

    # Set the window icon with the correct path
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))
    else:
        print(f"Logo file not found at {logo_path}")

    # Set global application font to "Palatino Linotype"
    app_font = QFont("Palatino Linotype", 12)
    app.setFont(app_font)

    # Set global styling with Palatino Linotype font and black text
    app.setStyleSheet("""
        QWidget {
            color: black;  /* Set text color to black */
            font-family: 'Palatino Linotype';  /* Use Palatino Linotype globally */
        }
        QPushButton {
            color: black;
            font-family: 'Palatino Linotype';
        }
        QLabel {
            color: black;
            font-family: 'Palatino Linotype';
        }
        QLineEdit {
            color: black;
            font-family: 'Palatino Linotype';
        }
        QComboBox {
            color: black;
            font-family: 'Palatino Linotype';
        }
        QTableView {
            color: black;
            font-family: 'Palatino Linotype';
        }
        QHeaderView::section {
            color: black;
            font-family: 'Palatino Linotype';
        }
        QTabBar::tab {
            color: black;
            font-family: 'Palatino Linotype';
        }
        QTabBar::tab:selected {
            background-color: lightgray;  /* Light gray on selection */
        }
    """)

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
