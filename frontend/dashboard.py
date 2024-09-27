from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QPushButton, QLabel, \
    QSplitter, QTableWidgetItem, QSizePolicy
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

LEFT_PANEL_WIDTH = 150  # Common width constant for left panel

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        # Create a splitter for the left (custom buttons) and right (tables) panels
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.splitter)

        # Left Panel: Create custom buttons instead of QTabWidget
        self.left_panel_widget = QWidget()
        self.left_panel_layout = QVBoxLayout()
        self.left_panel_widget.setLayout(self.left_panel_layout)

        # Set a fixed width for the left panel using the constant
        self.left_panel_widget.setFixedWidth(LEFT_PANEL_WIDTH)

        # Button-like tabs with icons and text
        self.summary_button = QPushButton("Summary")
        self.history_button = QPushButton("History")

        # Set icons to the buttons
        summary_icon = QIcon(r"..\images\dashboard\Summary.png")  # Replace with correct path
        history_icon = QIcon(r"..\images\dashboard\History.png")  # Replace with correct path
        self.summary_button.setIcon(summary_icon)
        self.history_button.setIcon(history_icon)

        # Set style for the buttons to make them flat and aligned
        self.summary_button.setFlat(True)
        self.summary_button.setIconSize(self.summary_button.sizeHint())
        self.history_button.setFlat(True)
        self.history_button.setIconSize(self.history_button.sizeHint())

        # Add buttons to the left panel layout
        self.left_panel_layout.addWidget(self.summary_button)
        self.left_panel_layout.addWidget(self.history_button)
        self.left_panel_layout.addStretch()  # Push buttons to the top

        # Add left panel to the splitter
        self.splitter.addWidget(self.left_panel_widget)

        # Right Panel: This is where the tables (Summary/History) will be shown
        self.right_panel = QWidget()
        self.right_panel_layout = QVBoxLayout()
        self.right_panel.setLayout(self.right_panel_layout)

        # Set width for the right panel using the constant
        self.right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Initially hide the right panel
        self.right_panel.setVisible(False)

        # Add right panel to the splitter
        self.splitter.addWidget(self.right_panel)

        # Table for summary details (will be shown in the right panel)
        self.summary_table = QTableWidget()
        self.summary_table.setRowCount(3)  # Example: 3 audit checks
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(['Check Name', 'Description'])
        self.summary_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Adding example audit check details
        self.summary_table.setItem(0, 0, QTableWidgetItem("Check for Config Files"))
        self.summary_table.setItem(0, 1, QTableWidgetItem("Verifies that all configuration files are in place."))
        self.summary_table.setItem(1, 0, QTableWidgetItem("Security Policies Compliance"))
        self.summary_table.setItem(1, 1, QTableWidgetItem("Ensures that all security policies are being followed."))
        self.summary_table.setItem(2, 0, QTableWidgetItem("Database Integrity"))
        self.summary_table.setItem(2, 1, QTableWidgetItem("Checks if the database maintains referential integrity."))

        # Table for audit history details
        self.audit_history_table = QTableWidget()
        self.audit_history_table.setRowCount(3)  # Example: 3 history entries
        self.audit_history_table.setColumnCount(3)
        self.audit_history_table.setHorizontalHeaderLabels(['Audit Name', 'Status', 'Date'])
        self.audit_history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.audit_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Load tick and cross images for status
        self.tick_pixmap = QPixmap(r"..\images\Issues\check.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.cross_pixmap = QPixmap(r"..\images\Issues\cross.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Adding example audit history details with images for status
        self.add_audit_history_row(0, "Initial Configuration Audit", True, "2024-09-01")
        self.add_audit_history_row(1, "Security Policy Audit", False, "2024-09-02")
        self.add_audit_history_row(2, "Database Integrity Check", True, "2024-09-03")

        # Connect buttons to switch content in the right panel
        self.summary_button.clicked.connect(lambda: self.switch_tab(0))
        self.history_button.clicked.connect(lambda: self.switch_tab(1))

    def switch_tab(self, index):
        """Switch the right panel content based on the selected tab."""
        # Hide the right panel if no valid tab is selected
        if index is None:
            self.right_panel.setVisible(False)
            return

        # Clear the right panel layout
        for i in reversed(range(self.right_panel_layout.count())):
            widget = self.right_panel_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Display the corresponding table based on the selected tab
        if index == 0:  # Summary Tab
            self.right_panel_layout.addWidget(self.summary_table)
        elif index == 1:  # History Tab
            self.right_panel_layout.addWidget(self.audit_history_table)

        # Show the right panel when a tab is selected
        self.right_panel.setVisible(True)

    def add_audit_history_row(self, row, audit_name, completed, date):
        self.audit_history_table.setItem(row, 0, QTableWidgetItem(audit_name))
        self.audit_history_table.setItem(row, 2, QTableWidgetItem(date))

        status_label = QLabel()
        if completed:
            status_label.setPixmap(self.tick_pixmap)
        else:
            status_label.setPixmap(self.cross_pixmap)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image in the cell
        self.audit_history_table.setCellWidget(row, 1, status_label)
