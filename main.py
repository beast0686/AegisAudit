import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget

from AuditR.UserLogins import UserManagement
from AuditR.Dashboard import Dashboard
from AuditR.Configuration import AuditConfiguration
from AuditR.ExecutionControl import ExecutionControl
from AuditR.Result import ResultsDisplay
from AuditR.Issues import IssueManagement

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

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

        self.user_management_tab = UserManagement()
        self.tab_widget.addTab(self.user_management_tab, "User Management")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
