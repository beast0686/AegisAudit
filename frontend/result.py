from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget,
                             QTableWidgetItem, QPushButton, QFileDialog, QMessageBox,
                             QLabel, QHBoxLayout, QHeaderView)  # Added QHeaderView import
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import csv


class ResultsDisplay(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tab Widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Programs Tab
        self.programs_tab = QWidget()
        self.programs_layout = QVBoxLayout()
        self.programs_tab.setLayout(self.programs_layout)
        self.tab_widget.addTab(self.programs_tab, "Programs")

        # List of Programs
        self.programs_table = QTableWidget()
        self.programs_table.setRowCount(5)  # Example: 5 programs
        self.programs_table.setColumnCount(1)
        self.programs_table.setHorizontalHeaderLabels(['Programs'])
        self.programs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.programs_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.programs_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.programs_layout.addWidget(self.programs_table)

        # Example Programs
        programs = ["Program A", "Program B", "Program C", "Program D", "Program E"]
        for i, program in enumerate(programs):
            self.programs_table.setItem(i, 0, QTableWidgetItem(program))

        # Checks Tab
        self.checks_tab = QWidget()
        self.checks_layout = QVBoxLayout()
        self.checks_tab.setLayout(self.checks_layout)
        self.tab_widget.addTab(self.checks_tab, "Checks")

        # Table for displaying check results
        self.checks_table = QTableWidget()
        self.checks_table.setRowCount(0)  # Start with 0 rows, will be populated based on selection
        self.checks_table.setColumnCount(2)
        self.checks_table.setHorizontalHeaderLabels(['Name', 'Status'])
        self.checks_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.checks_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.checks_layout.addWidget(self.checks_table)

        # Connect program selection to display checks
        self.programs_table.itemSelectionChanged.connect(self.display_checks)

        # Export Button at the bottom right
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_results)
        self.layout.addWidget(self.export_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Load tick and cross images
        self.tick_pixmap = QPixmap(r"..\images\Results\check.png")
        self.cross_pixmap = QPixmap(r"..\images\Results\cross.png")

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
