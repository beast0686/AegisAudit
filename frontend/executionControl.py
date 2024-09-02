from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QProgressBar, QTextEdit, QApplication
import time

class ExecutionControl(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.start_button = QPushButton("Start Audit")
        self.start_button.clicked.connect(self.start_audit)
        self.layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.console_output = QTextEdit()
        self.layout.addWidget(self.console_output)

    def start_audit(self):
        for i in range(101):
            self.progress_bar.setValue(i)
            self.console_output.append(f"Audit in progress... ({i}%)")
            QApplication.processEvents()
            time.sleep(0.01)
        self.console_output.append("Audit completed.")
