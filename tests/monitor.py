import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from QTermWidget import QTermWidget
from subprocess import Popen

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Embed htop in PyQt5")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.term_widget = QTermWidget()
        layout.addWidget(self.term_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.start_htop()

    def start_htop(self):
        self.htop_process = Popen(["htop"], stdout=self.term_widget.ptyMasterFd(), stderr=self.term_widget.ptyMasterFd())
        self.htop_process.wait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())

