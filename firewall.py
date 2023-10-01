import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from qtwidgets import Toggle

class UFWToggleApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('UFW Toggle')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.toggle_button = Toggle()
        self.toggle_button.setFixedWidth(55)
        # self.toggle_button.set_size(50)
        self.toggle_button.setChecked(self.isUFWActive())
        self.toggle_button.clicked.connect(self.toggleUFW)
        self.layout.addWidget(self.toggle_button)

        self.show()

    def isUFWActive(self):
        try:
            ufw_status = subprocess.check_output(["ufw", "status"]).decode()
            return "Status: active" in ufw_status
        except subprocess.CalledProcessError:
            return False

    def toggleUFW(self):
        try:
            if self.toggle_button.isChecked():
                subprocess.run(["sudo", "ufw", "enable"])
            else:
                subprocess.run(["sudo", "ufw", "disable"])
        except subprocess.CalledProcessError:
            pass  # Handle errors as needed

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UFWToggleApp()
    sys.exit(app.exec_())
