import sys
import os

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml") 
    engine = QQmlApplicationEngine()
    engine.load(os.path.join(os.path.dirname(__file__),"qml/main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())