from backend import ArduinoCommunication
from gui import MainWindow
from PySide6.QtWidgets import QApplication
import sys

def main():
    backend = ArduinoCommunication()
    if not backend.find_device():
        sys.exit(1)

    app = QApplication(sys.argv)
    w = MainWindow(backend)
    w.show()
    app.exec()


if __name__ == "__main__":
    main()