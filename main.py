import sys
import os,subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet
from qtwidgets import Toggle

class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()

        network_layout = QVBoxLayout()

        network_label = QLabel("Network")
        network_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        network_label.setStyleSheet("background-color: #232629;padding: 0px;font-size:24px;")
        network_label.setFixedHeight(50)
        network_layout.addWidget(network_label)

        ufw_section_layout = QHBoxLayout()
        ufw_label = QLabel("Ubuntu FireWall")
        ufw_label.setStyleSheet("color: white; background-color: #31363b;font-size: 18px;")

        self.ufw_toggle = Toggle()  # Use your custom Toggle widget
        self.ufw_toggle.setChecked(self.isUFWActive())  # Call isUFWActive to set the initial state
        self.ufw_toggle.clicked.connect(self.toggleUFW) # Connect the toggle action
        
        ufw_label.setFixedWidth(285)
        ufw_section_layout.addWidget(ufw_label)
        ufw_section_layout.addWidget(self.ufw_toggle)
        ufw_section_layout.addStretch(1)  # Pushes the toggle button to the right
        network_layout.addLayout(ufw_section_layout)

        self.status_label = QLabel("Firewall Status: ", self)
        self.status_label.setGeometry(20, 20, 200, 30)

        # Create buttons for various actions
        enable_button = QPushButton("Enable Firewall", self)
        enable_button.clicked.connect(self.enable_firewall)

        disable_button = QPushButton("Disable Firewall", self)
        disable_button.clicked.connect(self.disable_firewall)

        self.reset_button = QPushButton("Reset Firewall", self)
        self.reset_button.clicked.connect(self.reset_firewall)

        self.list_rules_button = QPushButton("List Rules", self)
        self.list_rules_button.clicked.connect(self.list_rules)

        self.add_rule_button = QPushButton("Add Rule", self)
        self.add_rule_button.clicked.connect(self.add_rule)

        self.delete_rule_button = QPushButton("Delete Rule", self)
        self.delete_rule_button.clicked.connect(self.delete_rule)

        # Create a QTextEdit widget to display rule listing and adding
        self.rules_text_edit = QTextBrowser(self)


        # network_layout.addWidget(self.status_label)
        # network_layout.addWidget(enable_button)
        # network_layout.addWidget(disable_button)
        network_layout.addWidget(self.list_rules_button)
        network_layout.addWidget(self.add_rule_button)
        network_layout.addWidget(self.delete_rule_button)
        network_layout.addWidget(self.reset_button)
        network_layout.addWidget(self.rules_text_edit)

        content_widget = QWidget()  # Create a widget to hold the content
        content_widget.setLayout(network_layout)

        scroll_area = QScrollArea()  # Create a scroll area
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Show vertical scrollbar
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide horizontal scrollbar
        scroll_area.setWidget(content_widget)  # Set the content widget for the scroll area

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #31363b;")
        # network_layout.addWidget(QLabel("Network Page Content"))
        # self.setStyleSheet("background-color: #232629;")
        # self.setLayout(network_layout)

    def isUFWActive(self):
        try:
            ufw_status = subprocess.check_output(["ufw", "status"]).decode()
            return "Status: active" in ufw_status
        except subprocess.CalledProcessError:
            return False

    def toggleUFW(self):
        try:
            self.ufw_toggle = self.sender()  # Get the sender widget (self.ufw_toggle checkbox)
            if self.ufw_toggle.isChecked():
                subprocess.run(["sudo", "ufw", "enable"])
            else:
                subprocess.run(["sudo", "ufw", "disable"])
            self.list_rules()
        except subprocess.CalledProcessError:
            pass  # Handle errors as needed

    
    def reset_firewall(self):
        subprocess.run(["sudo","ufw","--force","reset"])
        self.ufw_toggle.setChecked(False)
        self.list_rules()
        

    def enable_firewall(self):
        # Run the 'ufw enable' command as a subprocess with sudo
        subprocess.run(["sudo", "ufw", "enable"])

        # Update the status label to display the new firewall status
        self.list_rules()

    def disable_firewall(self):
        # Run the 'ufw disable' command as a subprocess with sudo
        subprocess.run(["sudo", "ufw", "disable"])

        # Update the status label to display the new firewall status
        self.list_rules()

    def list_rules(self):
        # Run the 'ufw status' command to list firewall rules
        rules_output = subprocess.getoutput("sudo ufw status numbered")
        self.rules_text_edit.setPlainText(rules_output)

    def add_rule(self):
        # Open a dialog to input a new rule
        new_rule, ok = QtWidgets.QInputDialog.getText(
            self, "Add Rule", "Enter a new firewall rule (e.g., allow 80/tcp):"
        )
        new_rule = new_rule.split()
        precommand = ['sudo','ufw']
        precommand.extend(new_rule)
        print(precommand)
        if ok:
            # Run the 'ufw allow' or 'ufw deny' command with the new rule
            subprocess.run(precommand)

            # Update the displayed rules
            self.list_rules()

    def delete_rule(self):
        # Open a dialog to input the rule to be deleted
        rule_to_delete, ok = QtWidgets.QInputDialog.getText(
            self, "Delete Rule", "Enter the firewall rule to delete:"
        )
        rule_to_delete = rule_to_delete.split()
        precommand = ['sudo','ufw','delete']
        precommand.extend(rule_to_delete)
        if ok:
            # Run the 'ufw delete' command to delete the specified rule
            subprocess.run(rule_to_delete)

            # Update the displayed rules
            self.list_rules()

    def update_status_label(self):
        # Retrieve the current firewall status using 'ufw status' command
        status = subprocess.getoutput("sudo ufw status | head -1")
        status = status.split()[-1]
        # Update the status label text to reflect the current status
        self.status_label.setText(f"Firewall Status: {status}")



class HardwarePage(QWidget):
    def __init__(self):
        super().__init__()

        hardware_layout = QVBoxLayout()

        hardware_label = QLabel("Hardware")
        hardware_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hardware_label.setStyleSheet("background-color:#232629; padding: 0px;font-size:24px;")
        hardware_label.setFixedHeight(50)
        hardware_layout.addWidget(hardware_label)
        self.disable_usb_button = QPushButton('Disable USB Ports', self)
        self.enable_button = QPushButton('Enable USB Ports', self)

        hardware_layout.addWidget(self.disable_usb_button)
        hardware_layout.addWidget(self.enable_button)

        self.disable_usb_button.clicked.connect(self.disable_usb_ports)
        self.enable_button.clicked.connect(self.enable_usb_ports)

        # Add other content to the hardwarePage
        hardware_layout.addWidget(QLabel(""))
        self.setLayout(hardware_layout)
    
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

class StoragePage(QWidget):
    def __init__(self):
        super().__init__()

        storage_layout = QVBoxLayout()

        storage_label = QLabel("Storage")
        storage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        storage_label.setStyleSheet("background-color:#232629; padding: 0px;font-size:24px;")

        storage_label.setFixedHeight(50)
        storage_layout.addWidget(storage_label)

        storage_layout.addWidget(QLabel(""))
        self.setLayout(storage_layout)

class MonitorPage(QWidget):
    def __init__(self):
        super().__init__()

        monitor_layout = QVBoxLayout()

        monitor_label = QLabel("Monitoring")
        monitor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monitor_label.setStyleSheet("background-color:#232629; padding: 0px;font-size:24px;")

        monitor_label.setFixedHeight(50)
        monitor_layout.addWidget(monitor_label)

        monitor_button = QPushButton('Start Monitoring', self)
        monitor_button.clicked.connect(self.start_monitoring)
        monitor_layout.addWidget(monitor_button)
        

        monitor_layout.addWidget(QLabel(""))
        self.setLayout(monitor_layout)

    def start_monitoring(self):
        try:
            # Replace 'gnome-terminal' with your preferred terminal emulator (e.g., 'xterm', 'konsole')
            subprocess.Popen(['xterm','-T','Monitoring','monitor'])
        except FileNotFoundError:
            # Handle the case where the terminal emulator is not found
            print("Terminal emulator not found. Please install one.")

class UpdatesPage(QWidget):
    def __init__(self):
        super().__init__()

        updates_layout = QVBoxLayout()

        updates_label = QLabel("System Updates")
        updates_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        updates_label.setStyleSheet("background-color:#232629; padding: 0px;font-size:24px;")
        updates_label.setFixedHeight(50)
        updates_layout.addWidget(updates_label)

        updates_section_layout = QHBoxLayout()
        updates_label = QLabel("Unattended Updates")
        updates_label.setStyleSheet("color: white; background-color: #31363b;font-size: 18px;")

        updates_toggle = Toggle()  
        updates_toggle.setChecked(self.is_update_enabled())  
        updates_toggle.clicked.connect(self.toggle_updates)  
        updates_label.setFixedWidth(285)
        updates_section_layout.addWidget(updates_label)
        updates_section_layout.addWidget(updates_toggle)
        updates_section_layout.addStretch(1)

        upgrades_section_layout = QHBoxLayout()
        upgrades_label = QLabel("Unattended Upgrades")
        upgrades_label.setStyleSheet("color: white; background-color: #31363b;font-size: 18px;")

        upgrades_toggle = Toggle()  
        upgrades_toggle.setChecked(self.is_update_enabled())  
        upgrades_toggle.clicked.connect(self.toggle_upgrades)  
        upgrades_label.setFixedWidth(285)
        upgrades_section_layout.addWidget(upgrades_label)
        upgrades_section_layout.addWidget(upgrades_toggle)
        upgrades_section_layout.addStretch(1)

        updates_layout.addLayout(updates_section_layout)
        updates_layout.addLayout(upgrades_section_layout)


        updates_layout.addWidget(QLabel(""))
        self.setStyleSheet("background-color: #31363b;")
        self.setLayout(updates_layout)

    def toggle_updates(self):
        try:
            if self.is_update_enabled():
                subprocess.run(["sudo", "sed", "-i", 's/APT::Periodic::Update-Package-Lists "1";/APT::Periodic::Update-Package-Lists "0";/', "/etc/apt/apt.conf.d/20auto-upgrades"])
            else:
                subprocess.run(["sudo", "sed", "-i", 's/APT::Periodic::Update-Package-Lists "0";/APT::Periodic::Update-Package-Lists "1";/', "/etc/apt/apt.conf.d/20auto-upgrades"])
        except subprocess.CalledProcessError:
            pass  # Handle errors as needed

    def toggle_upgrades(self):
        try:
            if self.is_upgrade_enabled():
                subprocess.run(["sudo", "sed", "-i", 's/APT::Periodic::Unattended-Upgrade "1";/APT::Periodic::Unattended-Upgrade "0";/', "/etc/apt/apt.conf.d/20auto-upgrades"])
            else:
                subprocess.run(["sudo", "sed", "-i", 's/APT::Periodic::Unattended-Upgrade "0";/APT::Periodic::Unattended-Upgrade "1";/', "/etc/apt/apt.conf.d/20auto-upgrades"])
        except subprocess.CalledProcessError:
            pass  # Handle errors as needed
    
    def is_update_enabled(self):
        try:
            # Run the command to check unattended-upgrades status
            result = subprocess.run(
                ["grep", "-q", 'APT::Periodic::Update-Package-Lists "1"', "/etc/apt/apt.conf.d/20auto-upgrades"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            return True  # If the command succeeds, unattended-upgrades are enabled
        except subprocess.CalledProcessError:
            return False  # If the command fails, unattended-upgrades are disabled


    def is_upgrade_enabled(self):
        try:
            # Run the command to check unattended-upgrades status
            result = subprocess.run(
                ["grep", "-q", 'APT::Periodic::Unattended-Upgrade "1"', "/etc/apt/apt.conf.d/20auto-upgrades"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            return True  # If the command succeeds, unattended-upgrades are enabled
        except subprocess.CalledProcessError:
            return False  # If the command fails, unattended-upgrades are disabled

class NavBar(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()

        # Hamburger menu button in the top-left corner
        # self.sidebar_button = QPushButton("☰")
        self.sidebar_button = QPushButton("Crypzard")
        self.sidebar_button.setStyleSheet("font-size: 24px; padding: 5px;")
        # self.sidebar_button.clicked.connect(self.toggle_sidebar)

        # Container widget for the button
        button_container = QWidget()
        button_container.setFixedWidth(200)
        button_container.setStyleSheet("background-color: #232629;")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.sidebar_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignJustify)
        button_container.setLayout(button_layout)
        self.layout.addWidget(button_container)
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)
        self.sidebar.setVisible(True)

        # List of menu items
        self.menu_list = QListWidget()
        self.menu_list.addItem("Network")
        self.menu_list.addItem("Hardware")
        self.menu_list.addItem("Storage")
        self.menu_list.addItem("Updates")
        self.menu_list.addItem("Monitor")

        for index in range(self.menu_list.count()):
            item = self.menu_list.item(index)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.menu_list.itemClicked.connect(self.menu_item_clicked)
        self.sidebar_layout.addWidget(self.menu_list)

        self.sidebar_layout.setContentsMargins(0,0,0,0)
        self.layout.setContentsMargins(0,0,0,0)
        self.sidebar.setFixedWidth(200)

        self.layout.addWidget(self.sidebar)
        self.setLayout(self.layout)

    # def toggle_sidebar(self):
    #     self.sidebar.setVisible(not self.sidebar.isVisible())

    def menu_item_clicked(self, item):
        selected_item_text = item.text()
        for index, page_text in enumerate(["Network", "Hardware", "Storage", "Updates", "Monitor"]):
            if selected_item_text == page_text:
                self.stacked_widget.setCurrentIndex(index)

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Crypzard")
        self.setFixedWidth(800)
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()  # Use a horizontal layout

        # Create a stacked widget to hold pages
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setFixedWidth(570)
        # Page widgets
        network_page = NetworkPage()
        hardware_page = HardwarePage()
        storage_page = StoragePage()
        updates_page = UpdatesPage()
        monitor_page = MonitorPage()


        self.stacked_widget.addWidget(network_page)
        self.stacked_widget.addWidget(hardware_page)
        self.stacked_widget.addWidget(storage_page)
        self.stacked_widget.addWidget(updates_page)
        self.stacked_widget.addWidget(monitor_page)

        self.navbar = NavBar(self.stacked_widget)

        # Add the navbar and stacked widget to the central widget
        self.layout.addWidget(self.navbar)
        self.layout.addWidget(self.stacked_widget)

        self.central_widget.setLayout(self.layout)

if __name__ == "__main__":
    if os.geteuid() != 0:
        # If not running as root, execute the run_as_root.sh scrip
        sys.exit("Failed to run the application with root privileges.")
    else:
        # Your application logic when running as root
        app = QApplication(sys.argv)
        apply_stylesheet(app,theme="dark_teal.xml")
        main_window = MainPage()
        main_window.show()
        sys.exit(app.exec_())