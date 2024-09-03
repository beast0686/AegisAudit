from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QProgressBar, QTextEdit, QApplication, QHBoxLayout
from PyQt6.QtCore import QTimer, QSize
from PyQt6.QtGui import QIcon
import sys


class ExecutionControl(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Progress bar at the top
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # Console output in the middle
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.layout.addWidget(self.console_output)

        # Horizontal layout for buttons (as images) at the bottom
        self.button_layout = QHBoxLayout()

        # Stop button with an icon
        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\Execution Control\stop.png"))
        self.stop_button.setIconSize(QSize(32, 32))
        self.stop_button.clicked.connect(self.stop_audit)
        self.button_layout.addWidget(self.stop_button)

        # Pause button with an icon
        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\Execution Control\pause.png"))
        self.pause_button.setIconSize(QSize(32, 32))
        self.pause_button.clicked.connect(self.pause_audit)
        self.button_layout.addWidget(self.pause_button)

        # Start button with an icon
        self.start_button = QPushButton()
        self.start_button.setIcon(QIcon(r"D:\BNMIT\Engineering CSE\SIH 2024\Local\images\Execution Control\play.png"))
        self.start_button.setIconSize(QSize(32, 32))
        self.start_button.clicked.connect(self.start_audit)
        self.button_layout.addWidget(self.start_button)

        self.layout.addLayout(self.button_layout)

        # Timer for controlling the audit process
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

        # Variables to manage the audit state
        self.progress = 0
        self.is_paused = False

    def start_audit(self):
        if not self.timer.isActive():
            if self.is_paused:
                self.console_output.append("Resuming audit...")
            else:
                self.console_output.append("Starting audit...")
            self.is_paused = False
            self.timer.start(100)  # Update every 100ms

    def pause_audit(self):
        if self.timer.isActive():
            self.is_paused = True
            self.timer.stop()
            self.console_output.append("Audit paused.")

    def stop_audit(self):
        self.timer.stop()
        self.progress = 0
        self.progress_bar.setValue(0)
        self.console_output.append("Audit stopped.")
        self.is_paused = False

    def update_progress(self):
        if not self.is_paused:
            if self.progress < 100:
                self.progress += 1
                self.progress_bar.setValue(self.progress)
                self.console_output.append(f"Audit in progress... ({self.progress}%)")
            else:
                self.timer.stop()
                self.console_output.append("Audit completed.")
                self.progress = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExecutionControl()
    window.show()
    sys.exit(app.exec())
