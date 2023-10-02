import sys
import os,subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
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

        ufw_toggle = Toggle()  # Use your custom Toggle widget
        ufw_toggle.setChecked(self.isUFWActive())  # Call isUFWActive to set the initial state
        ufw_toggle.clicked.connect(self.toggleUFW)  # Connect the toggle action
        ufw_label.setFixedWidth(285)
        ufw_section_layout.addWidget(ufw_label)
        ufw_section_layout.addWidget(ufw_toggle)
        ufw_section_layout.addStretch(1)  # Pushes the toggle button to the right
        network_layout.addLayout(ufw_section_layout)

        # Add other content to the NetworkPage
        for i in range(2):  # Add some content to demonstrate scrolling
            network_layout.addWidget(QLabel(f"Network Page Content {i}"))

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
            ufw_toggle = self.sender()  # Get the sender widget (ufw_toggle checkbox)
            if ufw_toggle.isChecked():
                subprocess.run(["sudo", "ufw", "enable"])
            else:
                subprocess.run(["sudo", "ufw", "disable"])
        except subprocess.CalledProcessError:
            pass  # Handle errors as needed



class HardwarePage(QWidget):
    def __init__(self):
        super().__init__()

        network_layout = QVBoxLayout()

        network_label = QLabel("Hardware")
        network_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        network_label.setStyleSheet(" padding: 0px;font-size:24px;")
        network_label.setFixedHeight(50)
        network_layout.addWidget(network_label)

        # Add other content to the NetworkPage
        network_layout.addWidget(QLabel("Hardware Page Content"))
        self.setStyleSheet("background-color: #232629;")
        self.setLayout(network_layout)
class StoragePage(QWidget):
    def __init__(self):
        super().__init__()

        storage_layout = QVBoxLayout()

        storage_label = QLabel("Storage")
        storage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        storage_label.setStyleSheet(" padding: 0px;font-size:24px;")
        storage_label.setFixedHeight(50)
        storage_layout.addWidget(storage_label)

        storage_layout.addWidget(QLabel("Storage Page Content"))
        self.setStyleSheet("background-color: #232629;")
        self.setLayout(storage_layout)

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
        for index, page_text in enumerate(["Network", "Hardware", "Storage", "Updates"]):
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

        self.stacked_widget.addWidget(network_page)
        self.stacked_widget.addWidget(hardware_page)
        self.stacked_widget.addWidget(storage_page)
        self.stacked_widget.addWidget(updates_page)

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