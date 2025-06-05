import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_design import Ui_MainWindow  # Import your generated UI class


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.setFixedSize(1600, 900)
        self.ui.setupUi(self)


        # (Optional) Connect button signals here
        # Example: self.ui.pushButton_search.clicked.connect(self.handle_search)

        # Show the window
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())