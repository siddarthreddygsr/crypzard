import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import psutil
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qt_material import apply_stylesheet

class StoragePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        storage_layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Storage Page")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding-bottom: 10px;")
        storage_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create a scroll area to contain the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the widget to resize with the scroll area
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Display disk information
        disk_info_label = QLabel("Disk Information")
        disk_info_label.setStyleSheet("font-size: 16px; font-weight: bold; padding-top: 10px;")
        scroll_layout.addWidget(disk_info_label)

        for partition in psutil.disk_partitions():
            partition_info_label = QLabel(f"Device: {partition.device}\n"
                                          f"Mount Point: {partition.mountpoint}\n"
                                          f"File System: {partition.fstype}")
            scroll_layout.addWidget(partition_info_label)

        # Create pie chart for disk usage
        disk_usage_label = QLabel("Disk Usage")
        disk_usage_label.setStyleSheet("font-size: 16px; font-weight: bold; padding-top: 10px;")
        scroll_layout.addWidget(disk_usage_label)

        usage_data = self.get_disk_usage_data()
        pie_chart = self.create_pie_chart(usage_data)
        scroll_layout.addWidget(pie_chart)

        # Disk cleanup button
        cleanup_button = QPushButton('Clean Up Disk')
        cleanup_button.clicked.connect(self.cleanup_disk)
        cleanup_button.setStyleSheet("font-size: 16px; background-color: #4CAF50; color: white; padding: 10px;")
        scroll_layout.addWidget(cleanup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set the scroll content widget in the scroll area
        scroll_area.setWidget(scroll_content)
        storage_layout.addWidget(scroll_area)

        self.setLayout(storage_layout)

    def get_disk_usage_data(self):
        usage_data = []
        for partition in psutil.disk_partitions():
            if not partition.mountpoint.startswith('/snap'):
                usage = psutil.disk_usage(partition.mountpoint)
                usage_data.append((partition.mountpoint, usage.used / usage.total))

        return usage_data

    def create_pie_chart(self, data):
        fig, ax = plt.subplots()
        labels, sizes = zip(*data)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Save the pie chart as an image and convert to a QPixmap for display
        buf = BytesIO()
        plt.savefig(buf, format='png')
        pie_chart_image = QPixmap()
        pie_chart_image.loadFromData(buf.getvalue())
        buf.close()

        pie_chart_label = QLabel()
        pie_chart_label.setPixmap(pie_chart_image)
        canvas = FigureCanvas(fig)
        return pie_chart_label

    def cleanup_disk(self):
        # Implement disk cleanup logic here
        # You can add code to delete temporary files, old backups, etc.
        pass

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")
    window = QMainWindow()
    storage_page = StoragePage()
    window.setCentralWidget(storage_page)
    window.setWindowTitle("Storage Page")
    
    # Set an application icon (customize the path)
    icon = QIcon(QPixmap("your_icon.png"))
    window.setWindowIcon(icon)
    
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
