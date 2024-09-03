from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget,
                             QPushButton, QFileDialog, QTableWidgetItem, QMessageBox, QLabel, QHBoxLayout)
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

        # List of Programs (as a placeholder QLabel, replace with actual list if needed)
        self.programs_list = QLabel("List of all test Programs")
        self.programs_list.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.programs_layout.addWidget(self.programs_list)

        # Checks Tab
        self.checks_tab = QWidget()
        self.checks_layout = QVBoxLayout()
        self.checks_tab.setLayout(self.checks_layout)
        self.tab_widget.addTab(self.checks_tab, "Checks")

        # Load tick and cross images
        tick_pixmap = QPixmap(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\check.png")
        cross_pixmap = QPixmap(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\cross.png")

        # Example parameters and their results
        parameters = [
            ("Parameter 1", True),
            ("Parameter 2", True),
            ("Parameter 3", False),
            ("Parameter 4", False),
            ("Parameter 5", True)
        ]

        # Layout for each check result
        for param, passed in parameters:
            param_layout = QHBoxLayout()
            param_label = QLabel(param)
            param_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            param_layout.addWidget(param_label)

            mark_label = QLabel()
            if passed:
                mark_label.setPixmap(tick_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                mark_label.setPixmap(cross_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio))
            param_layout.addWidget(mark_label)
            param_layout.addStretch()

            self.checks_layout.addLayout(param_layout)

        # Export Button at the bottom right
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_results)
        self.layout.addWidget(self.export_button, alignment=Qt.AlignmentFlag.AlignRight)

    def export_results(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Issue", "Severity", "Description"])
                # Assuming data is coming from somewhere, add logic to fetch data
                writer.writerow(["Example Issue", "High", "This is a sample description"])
            QMessageBox.information(self, "Results Exported", "Audit results have been exported.")
