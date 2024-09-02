from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QAbstractItemView, QHeaderView

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.summary_label = QLabel("Summary Section")
        self.layout.addWidget(self.summary_label)

        self.audit_history_label = QLabel("Audit History")
        self.layout.addWidget(self.audit_history_label)

        self.audit_history_table = QTableWidget()
        self.audit_history_table.setRowCount(0)
        self.audit_history_table.setColumnCount(3)
        self.audit_history_table.setHorizontalHeaderLabels(['Audit Name', 'Status', 'Date'])
        self.audit_history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.audit_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.audit_history_table)
