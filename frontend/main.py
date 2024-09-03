import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget

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

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create the tabs in the specified order
        self.user_management_tab = UserManagement()
        self.tab_widget.addTab(self.user_management_tab, "User Management")

        self.dashboard_tab = Dashboard()
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")

        self.audit_config_tab = AuditConfiguration()
        self.tab_widget.addTab(self.audit_config_tab, "Audit Configuration")

        self.execution_control_tab = ExecutionControl()
        self.tab_widget.addTab(self.execution_control_tab, "Execution Control")

        self.results_display_tab = ResultsDisplay()
        self.tab_widget.addTab(self.results_display_tab, "Results Display")

        self.issue_management_tab = IssueManagement()
        self.tab_widget.addTab(self.issue_management_tab, "Issue Management")

        # Disable all tabs except User Management by default
        self.enable_tabs(False)

        # Connect user management login signal
        self.user_management_tab.user_logged_in.connect(self.on_user_logged_in)

    def enable_tabs(self, enable):
        # Enable or disable all tabs except User Management
        for i in range(1, self.tab_widget.count()):
            self.tab_widget.setTabEnabled(i, enable)

    def on_user_logged_in(self):
        # Enable other tabs when a user is logged in
        self.enable_tabs(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
