import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox

class USBPortControl(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('USB Port Control')
        self.setGeometry(100, 100, 300, 100)

        self.disable_button = QPushButton('Disable USB Ports', self)
        self.enable_button = QPushButton('Enable USB Ports', self)

        layout = QVBoxLayout()
        layout.addWidget(self.disable_button)
        layout.addWidget(self.enable_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.disable_button.clicked.connect(self.disable_usb_ports)
        self.enable_button.clicked.connect(self.enable_usb_ports)

    def run_command(self, command):
        try:
            subprocess.run(['sudo', 'sh', '-c', command])
        except subprocess.CalledProcessError:
            self.show_message('Error', 'Failed to run the command.')
    def overwrite_rule(self, rule):
        try:
            with open('/etc/udev/rules.d/99-disable-usb.rules', 'w') as rule_file:
                rule_file.write(rule + '\n')
        except PermissionError:
            self.show_message('Error', 'Permission denied. Make sure to run as superuser (e.g., with "sudo").')

    def disable_usb_ports(self):
        self.run_command('sudo systemctl stop udev')
        self.overwrite_rule("""
SUBSYSTEMS=="usb", ATTRS{idVendor}=="*", ATTRS{idProduct}=="*", RUN="/bin/sh -c 'echo 0 >/sys/\$devpath/authorized'"
                         """)
        self.reload_udev_rules()
        self.run_command('sudo systemctl start udev')

    def enable_usb_ports(self):
        self.run_command('sudo systemctl stop udev')
        self.overwrite_rule("")
        self.reload_udev_rules()
        self.run_command('sudo systemctl start udev')

    def reload_udev_rules(self):
        try:
            subprocess.run(['sudo', 'udevadm', 'control', '--reload-rules'])
        except subprocess.CalledProcessError:
            self.show_message('Error', 'Failed to reload udev rules.')

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

def main():
    app = QApplication(sys.argv)
    window = USBPortControl()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
