import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLineEdit, QListWidget, QDateTimeEdit, QSizePolicy, QGroupBox, QFormLayout)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from datetime import datetime, timedelta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Log browser')
        self.setWindowIcon(QIcon('./assets/app_icon2.png'))
        self.setGeometry(75, 75, 1300, 700)

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
        
        self.num_of_logs = QLabel("Number of loaded logs: 0")

        self.status_bar = self.statusBar()
        self.status_bar.addWidget(self.num_of_logs)
        self.status_bar.setStyleSheet('background-color: #454f5e;')

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        work_space_layout.addWidget(main_widget)



class FileSearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("FileSearchWidget") 
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
        self.from_date.setDateTime(datetime.now() - timedelta(days=1))

        self.to_label = QLabel('To', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.to_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.to_date = QDateTimeEdit()
        self.to_date.setDateTime(datetime.now())

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

        self.timestamp_label = QLabel("-", wordWrap=True)
        self.uid_label = QLabel("-", wordWrap=True)
        self.level_label = QLabel("-", wordWrap=True)
        self.message_label = QLabel("-", wordWrap=True)
        self.host_ip_label = QLabel("-", wordWrap=True)
        self.host_port_label = QLabel("-", wordWrap=True)
        self.server_ip_label = QLabel("-", wordWrap=True)
        self.server_port_label = QLabel("-", wordWrap=True)
        self.trans_depth_label = QLabel("-", wordWrap=True)
        self.method_label = QLabel("-", wordWrap=True)
        self.host_label = QLabel("-", wordWrap=True)
        self.uri_label = QLabel("-", wordWrap=True)
        self.referrer_label = QLabel("-", wordWrap=True)
        self.user_agent_label = QLabel("-", wordWrap=True)
        self.request_body_len_label = QLabel("-", wordWrap=True)
        self.response_body_len_label = QLabel("-", wordWrap=True)
        self.status_code_label = QLabel("-", wordWrap=True)
        self.status_msg_label = QLabel("-", wordWrap=True)
        self.info_code_label = QLabel("-", wordWrap=True)
        self.info_msg_label = QLabel("-", wordWrap=True)
        self.filename_label = QLabel("-", wordWrap=True)
        self.tags_label = QLabel("-", wordWrap=True)
        self.username_label = QLabel("-", wordWrap=True)
        self.password_label = QLabel("-", wordWrap=True)
        self.proxied_label = QLabel("-", wordWrap=True)
        self.orig_fuids_label = QLabel("-", wordWrap=True)
        self.orig_mime_types_label = QLabel("-", wordWrap=True)
        self.resp_fuids_label = QLabel("-", wordWrap=True)
        self.resp_mime_types_label = QLabel("-", wordWrap=True)

        layout.addRow("Timestamp:", self.timestamp_label)
        layout.addRow("UID:", self.uid_label)
        layout.addRow("Level:", self.level_label)
        layout.addRow("Message:", self.message_label)
        layout.addRow("Host IP:", self.host_ip_label)
        layout.addRow("Host Port:", self.host_port_label)
        layout.addRow("Server IP:", self.server_ip_label)
        layout.addRow("Server Port:", self.server_port_label)
        layout.addRow("Trans Depth:", self.trans_depth_label)
        layout.addRow("Method:", self.method_label)
        layout.addRow("Host:", self.host_label)
        layout.addRow("URI:", self.uri_label)
        layout.addRow("Referrer:", self.referrer_label)
        layout.addRow("User Agent:", self.user_agent_label)
        layout.addRow("Request Body Length:", self.request_body_len_label)
        layout.addRow("Response Body Length:", self.response_body_len_label)
        layout.addRow("Status Code:", self.status_code_label)
        layout.addRow("Status Message:", self.status_msg_label)
        layout.addRow("Info Code:", self.info_code_label)
        layout.addRow("Info Message:", self.info_msg_label)
        layout.addRow("Filename:", self.filename_label)
        layout.addRow("Tags:", self.tags_label)
        layout.addRow("Username:", self.username_label)
        layout.addRow("Password:", self.password_label)
        layout.addRow("Proxied:", self.proxied_label)
        layout.addRow("Orig FUIds:", self.orig_fuids_label)
        layout.addRow("Orig MIME Types:", self.orig_mime_types_label)
        layout.addRow("Resp FUIds:", self.resp_fuids_label)
        layout.addRow("Resp MIME Types:", self.resp_mime_types_label)


        self.setLayout(layout)


class LogContentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()
    
    def __init_ui(self):
        main_layout = QVBoxLayout()
        # main_layout.setContentsMargins(10, 10, 10, 50)

        self.log_content_widget = QListWidget()
        self.log_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        main_layout.addWidget(self.log_content_widget)
        self.setLayout(main_layout)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet("""
    QWidget {
        font-family: 'Segoe UI';
        font-size: 12px;
    }
""")


    window = MainWindow()
    window.show()
    app.exec()
