import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from qt_material import apply_stylesheet
class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()

        network_layout = QVBoxLayout()
        network_layout.addWidget(QLabel("Network Page Content"))
        self.setLayout(network_layout)

class HardwarePage(QWidget):
    def __init__(self):
        super().__init__()

        hardware_layout = QVBoxLayout()
        hardware_layout.addWidget(QLabel("Hardware Page Content"))
        self.setLayout(hardware_layout)

class StoragePage(QWidget):
    def __init__(self):
        super().__init__()

        storage_layout = QVBoxLayout()
        storage_layout.addWidget(QLabel("Storage Page Content"))
        self.setLayout(storage_layout)

class UpdatesPage(QWidget):
    def __init__(self):
        super().__init__()

        updates_layout = QVBoxLayout()
        updates_layout.addWidget(QLabel("Updates Page Content"))
        self.setLayout(updates_layout)

class NavBar(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        self.layout = QVBoxLayout()

        # Hamburger menu button in the top-left corner
        # self.sidebar_button = QPushButton("☰")
        self.sidebar_button = QPushButton("Crypzard")
        self.sidebar_button.setStyleSheet("font-size: 24px; padding: 5px;")
        self.sidebar_button.clicked.connect(self.toggle_sidebar)

        # Container widget for the button
        button_container = QWidget()
        button_container.setFixedWidth(200)
        button_container.setStyleSheet("background-color: #232629;")  # Use the secondaryColor
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
        self.menu_list.itemClicked.connect(self.menu_item_clicked)
        self.sidebar_layout.addWidget(self.menu_list)

        self.sidebar_layout.setContentsMargins(0,0,0,0)
        self.layout.setContentsMargins(0,0,0,0)
        self.sidebar.setFixedWidth(200)
        

        self.layout.addWidget(self.sidebar)
        self.setLayout(self.layout)

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def menu_item_clicked(self, item):
        selected_item_text = item.text()
        for index, page_text in enumerate(["Network", "Hardware", "Storage", "Updates"]):
            if selected_item_text == page_text:
                self.stacked_widget.setCurrentIndex(index)

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Crypzard")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()  # Use a horizontal layout

        # Create a stacked widget to hold pages
        self.stacked_widget = QStackedWidget(self)

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
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")
    main_window = MainPage()
    main_window.show()
    sys.exit(app.exec_())
