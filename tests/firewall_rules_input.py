import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton

class DynamicInputApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynamic Input Fields")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.row_container = QVBoxLayout()  # Container for rows
        self.layout.addLayout(self.row_container)

        self.add_input_row()

        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.add_input_row)
        self.layout.addWidget(self.add_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

    def add_input_row(self):
        row_layout = QHBoxLayout()

        input_fields = []
        for _ in range(3):
            input_field = QLineEdit()
            row_layout.addWidget(input_field)
            input_fields.append(input_field)

        self.row_container.addLayout(row_layout)

    def save_data(self):
        data = []
        for row_index in range(self.row_container.count()):
            row_layout = self.row_container.itemAt(row_index)
            row_data = [field.text() for field in row_layout]  # Collect data from the fields in this row
            data.append(row_data)

        print("Saved data:", data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicInputApp()
    window.show()
    sys.exit(app.exec_())
