import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget

class BpytopLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Launch bpytop')
        self.setGeometry(100, 100, 300, 100)

        self.launch_button = QPushButton('Launch bpytop', self)
        layout = QVBoxLayout()
        layout.addWidget(self.launch_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.launch_button.clicked.connect(self.launch_bpytop)

    def launch_bpytop(self):
        try:
            subprocess.Popen(['xterm', '-geometry', '200x50', '-e', 'bpytop'])
        except FileNotFoundError:
            # Handle the case where the terminal emulator is not found
            print("Terminal emulator not found. Please install one.")

def main():
    app = QApplication(sys.argv)
    window = BpytopLauncher()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
