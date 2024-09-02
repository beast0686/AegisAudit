from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QFileDialog, QTableWidgetItem, QMessageBox
import csv

class ResultsDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.results_table = QTableWidget()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(['Issue', 'Severity', 'Description'])
        self.layout.addWidget(self.results_table)

        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.layout.addWidget(self.export_button)

    def export_results(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Issue", "Severity", "Description"])
                for row in range(self.results_table.rowCount()):
                    writer.writerow([self.results_table.item(row, 0).text(), self.results_table.item(row, 1).text(), self.results_table.item(row, 2).text()])
            QMessageBox.information(self, "Results Exported", "Audit results have been exported.")
