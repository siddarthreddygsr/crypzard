import sys
from PySide6 import QtGui


if __name__ == '__main__':
    app = QtGui.QGuiApplication(sys.argv)
    button = QtGui.QPushButton("Hello world")
    button.setCheckable(True)
    button.setStyleSheet("""
        QPushButton {background:rgb(65,66,66); color: white;} 
        QPushButton::checked{background:rgb(255, 0, 0); color: white;}
    """)
    button.show()
    sys.exit(app.exec_())