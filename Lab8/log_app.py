import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QGridLayout, QLineEdit, QListWidget, QDateTimeEdit, QSizePolicy, QGroupBox, QFormLayout)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Log browser')
        self.setWindowIcon(QIcon('./assets/app_icon2.png'))
        self.setGeometry(250, 150, 1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        work_space_layout = QVBoxLayout(central_widget)
        work_space_layout.setContentsMargins(5, 5, 5, 5)

        self.searching_widget = FileSearchWidget()
        work_space_layout.addWidget(self.searching_widget)

        self.date_choice_widget = DateSelectWidget()
        self.log_content_widget = LogContentWidget()

        master_info_layout = QVBoxLayout()
        master_info_layout.addWidget(self.date_choice_widget)
        master_info_layout.addWidget(self.log_content_widget, 3)

        self.log_content_manager_widget = LogContentManagerWidget()
        master_info_layout.addWidget(self.log_content_manager_widget)

        main_layout = QHBoxLayout()
        main_layout.addLayout(master_info_layout, 5)

        log_info_group = QGroupBox("Log content")
        log_info_group.setLayout(QVBoxLayout())
        self.log_details_widget = LogDetailsWidget()
        log_info_group.layout().addWidget(self.log_details_widget)
        main_layout.addWidget(log_info_group, 2)
        

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        work_space_layout.addWidget(main_widget)



class FileSearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()
    
    def __init_ui(self):
        main_layout = QHBoxLayout()

        self.path_input = QLineEdit(placeholderText='Insert log file path', clearButtonEnabled=True)
        self.browse_button = QPushButton('...')
        self.browse_button.setMaximumWidth(30)
        self.open_button = QPushButton('Open')

        main_layout.addWidget(self.path_input, 1)
        main_layout.addWidget(self.browse_button)
        main_layout.addWidget(self.open_button)
        self.setLayout(main_layout)        
    
class DateSelectWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()
    
    def __init_ui(self):
        main_layout = QHBoxLayout()

        self.from_label = QLabel('From', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.from_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.from_date = QDateTimeEdit()

        self.to_label = QLabel('To', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.to_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.to_date = QDateTimeEdit()

        self.filter_button = QPushButton('Filter')

        main_layout.addWidget(self.from_label)
        main_layout.addWidget(self.from_date)
        main_layout.addWidget(self.to_label)
        main_layout.addWidget(self.to_date)
        main_layout.addStretch()
        main_layout.addWidget(self.filter_button)
        self.setLayout(main_layout)

class LogContentManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()
    
    def __init_ui(self):
        main_layout = QHBoxLayout()

        self.next_button = QPushButton('Next')
        self.prev_button = QPushButton('Previous')

        main_layout.addWidget(self.prev_button)
        main_layout.addStretch()
        main_layout.addWidget(self.next_button)
        self.setLayout(main_layout)

class LogDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        layout = QFormLayout()  # automatycznie tworzy kolumnę "nazwa - wartość"

        self.timestamp_label = QLabel("-")
        self.uid_label = QLabel("-")
        self.level_label = QLabel("-")
        self.message_label = QLabel("-")

        layout.addRow("Timestamp:", self.timestamp_label)
        layout.addRow("UID:", self.uid_label)
        layout.addRow("Level:", self.level_label)
        layout.addRow("Message:", self.message_label)

        self.setLayout(layout)

class LogContentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()
    
    def __init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 0)

        self.log_content_widget = QListWidget()
        self.log_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        main_layout.addWidget(self.log_content_widget)
        self.setLayout(main_layout)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
