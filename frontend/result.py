from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QMessageBox,
                             QLabel, QHBoxLayout, QSplitter, QSpacerItem, QSizePolicy, QHeaderView)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
import csv

class ResultsDisplay(QWidget):
    def __init__(self):
        super().__init__()

        # Load the tick and cross pixmaps
        self.tick_pixmap = QPixmap(r"..\images\Results\check.png")
        self.cross_pixmap = QPixmap(r"..\images\Results\cross.png")

        # Create a splitter for the left (custom buttons) and right (tables) panels
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.splitter)

        # Left Panel: Create custom buttons for Programs and Checks
        self.left_panel_widget = QWidget()
        self.left_panel_layout = QVBoxLayout()
        self.left_panel_widget.setLayout(self.left_panel_layout)

        # Set fixed width for the left panel
        self.left_panel_widget.setFixedWidth(150)  # Adjust the width value as needed

        # Programs and Checks buttons with icons
        self.programs_button = QPushButton(" Programs")
        self.checks_button = QPushButton(" Checks")

        # Set icons to the buttons
        programs_icon = QIcon(r"..\images\Results\program.png")
        checks_icon = QIcon(r"..\images\Results\Checks.png")
        self.programs_button.setIcon(programs_icon)
        self.checks_button.setIcon(checks_icon)

        # Set style for the buttons to make them flat and aligned
        self.programs_button.setFlat(True)
        self.programs_button.setIconSize(self.programs_button.sizeHint())
        self.checks_button.setFlat(True)
        self.checks_button.setIconSize(self.checks_button.sizeHint())

        # Add buttons to the left panel layout
        self.left_panel_layout.addWidget(self.programs_button)
        self.left_panel_layout.addWidget(self.checks_button)
        self.left_panel_layout.addStretch()  # Push buttons to the top

        # Add left panel to the splitter
        self.splitter.addWidget(self.left_panel_widget)
        self.splitter.setStretchFactor(0, 1)

        # Right Panel: This is where the tables (Programs/Checks) will be shown
        self.right_panel = QWidget()
        self.right_panel_layout = QVBoxLayout()
        self.right_panel.setLayout(self.right_panel_layout)

        # Initially, hide the right panel
        self.right_panel.setVisible(False)

        # Programs Table
        self.programs_table = QTableWidget()
        self.programs_table.setRowCount(5)  # Example: 5 programs
        self.programs_table.setColumnCount(1)
        self.programs_table.setHorizontalHeaderLabels(['Programs'])
        self.programs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.programs_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.programs_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Example Programs
        programs = ["Program A", "Program B", "Program C", "Program D", "Program E"]
        for i, program in enumerate(programs):
            self.programs_table.setItem(i, 0, QTableWidgetItem(program))

        # Checks Table (will be shown when a program is selected)
        self.checks_table = QTableWidget()
        self.checks_table.setRowCount(0)  # Start with 0 rows, will be populated based on selection
        self.checks_table.setColumnCount(2)
        self.checks_table.setHorizontalHeaderLabels(['Name', 'Status'])
        self.checks_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.checks_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Add right panel to the splitter
        self.splitter.addWidget(self.right_panel)
        self.splitter.setStretchFactor(1, 2)

        # Initially hide the right panel content
        self.right_panel.setVisible(False)

        # Connect buttons to switch between programs and checks table
        self.programs_button.clicked.connect(lambda: self.switch_tab(0))
        self.checks_button.clicked.connect(lambda: self.switch_tab(1))

        # Connect program selection to display checks
        self.programs_table.itemSelectionChanged.connect(self.display_checks)

        # Export Button at the bottom right
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_results)
        self.layout.addWidget(self.export_button, alignment=Qt.AlignmentFlag.AlignRight)

    def switch_tab(self, index):
        """Switch the right panel content based on the selected tab."""
        # Clear the right panel layout
        for i in reversed(range(self.right_panel_layout.count())):
            widget = self.right_panel_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Display the corresponding table based on the selected tab
        if index == 0:  # Programs Tab
            self.right_panel_layout.addWidget(self.programs_table)
        elif index == 1:  # Checks Tab
            self.right_panel_layout.addWidget(self.checks_table)

        # Show the right panel when a tab is selected
        self.right_panel.setVisible(True)

    def display_checks(self):
        # Get selected program
        selected_items = self.programs_table.selectedItems()
        if not selected_items:
            return
        selected_program = selected_items[0].text()

        # Example checks for the selected program
        program_checks = {
            "Program A": [("Check 1", True), ("Check 2", False)],
            "Program B": [("Check 1", True), ("Check 3", True)],
            "Program C": [("Check 2", False), ("Check 4", True)],
            "Program D": [("Check 1", False), ("Check 2", True)],
            "Program E": [("Check 5", True), ("Check 3", False)]
        }

        # Get checks for the selected program
        checks = program_checks.get(selected_program, [])

        # Clear the existing rows in the checks table
        self.checks_table.setRowCount(0)

        # Populate the checks table with the checks for the selected program
        for check_name, passed in checks:
            row_position = self.checks_table.rowCount()
            self.checks_table.insertRow(row_position)

            # Set the check name
            self.checks_table.setItem(row_position, 0, QTableWidgetItem(check_name))

            # Set the status with tick or cross
            status_item = QLabel()
            if passed:
                pixmap = self.tick_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)
            else:
                pixmap = self.cross_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)

            status_item.setPixmap(pixmap)
            status_item.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image in the cell
            self.checks_table.setCellWidget(row_position, 1, status_item)

    def export_results(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Issue", "Severity", "Description"])
                # Assuming data is coming from somewhere, add logic to fetch data
                writer.writerow(["Example Issue", "High", "This is a sample description"])
            QMessageBox.information(self, "Results Exported", "Audit results have been exported.")
