import sys

from PyQt5.QtWidgets import QMessageBox
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLineEdit, QListWidget, QDateTimeEdit, QSizePolicy, QGroupBox, QFormLayout,
                               QFileDialog, QListView, QListWidgetItem)
from PySide6.QtGui import QIcon
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt, Signal
from datetime import datetime, timedelta
from log_parser import parse_log
from log_filter_by_timestamp import get_entries_by_timestamp
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.last_loaded_path = None
        self.lookup_from_string = None

        self.setWindowTitle('Log browser')
        self.setWindowIcon(QIcon('./assets/app_icon2.png'))
        self.setGeometry(50, 50, 1300, 850)

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

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Number of loaded logs:"))
        self.num_of_logs_label = QLabel("0")
        self.num_of_logs_label.setMinimumWidth(15)
        self.num_of_logs_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.num_of_logs_label)
        layout.setContentsMargins(10, 0, 10, 0)

        num_of_logs_widget = QWidget()
        num_of_logs_widget.setLayout(layout)
        self.status_bar = self.statusBar()
        self.status_bar.addWidget(num_of_logs_widget)
        self.status_bar.setStyleSheet('background-color: #454f5e;')

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        work_space_layout.addWidget(main_widget)

        self.searching_widget.search.connect(self.handle_search)
        self.searching_widget.browse.connect(self.handle_browse)
        self.date_choice_widget.filtering.connect(self.handle_filtering)
        self.log_content_widget.selected.connect(self.handle_selected)
        self.log_content_widget.deselected.connect(self.handle_deselected)
        self.log_content_manager_widget.next.connect(self.log_content_widget.next)
        self.log_content_manager_widget.prev.connect(self.log_content_widget.prev)


    def handle_search(self, path):
        if self.last_loaded_path == path:
            return
        try:
            with open(path, 'r') as file:
                result = parse_log(file, convert=False)
            self.last_loaded_path = path
            string_result = []
            for row in result:
                string_result.append(self.makeLabel(row))
            self.lookup_from_string = dict(zip(string_result, result))
            self.date_choice_widget.set_dates(
                datetime.fromtimestamp(float(result[0][0])),
                datetime.fromtimestamp(float(result[len(result) - 1][0]))
            )
            self.date_choice_widget.handle_filtering()
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'File not found.')
        except Exception:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect file format')
        


    def handle_browse(self):
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a File",
            dir = os.getcwd(),
            filter="Log Files (*.log)"
        )
        if file_path:
            self.searching_widget.set_field(file_path)
            self.handle_search(file_path)

    def handle_filtering(self, timestamp_begin, timestamp_end):
        if self.lookup_from_string is None:
            QtWidgets.QMessageBox.critical(self, 'Error', 'No log loaded.')
            return
        logs = list(self.lookup_from_string.values())
        filtered_logs = get_entries_by_timestamp(logs, timestamp_begin, timestamp_end)
        content = [self.makeLabel(log) for log in filtered_logs]
        self.log_content_widget.set_content(content)
        self.num_of_logs_label.setText(str(len(content)))
        if len(content) == 0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No entries found.')
        self.log_details_widget.clear()

    def handle_selected(self, text, row, number):
        log = self.lookup_from_string[text]
        self.log_details_widget.set_content(log)
        self.log_content_manager_widget.set_enabled_next(row != number - 1)
        self.log_content_manager_widget.set_enabled_prev(row != 0)

    def handle_deselected(self):
        self.log_details_widget.clear()
        self.log_content_manager_widget.set_enabled_next(False)
        self.log_content_manager_widget.set_enabled_prev(False)

    def makeLabel(self, row):
        font_stuff, width = self.log_content_widget.get_content_metrics()
        elided = font_stuff.elidedText(", ".join(row), Qt.ElideRight, width)
        if len(elided) > 0 and elided[-1] != '\n':
            elided += '\n'
        return elided


class FileSearchWidget(QWidget):
    search = Signal(str)
    browse = Signal()

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
        self.path_input.returnPressed.connect(self.handle_search)
        self.browse_button.clicked.connect(self.handle_browse)
        self.open_button.clicked.connect(self.handle_search)
        

        main_layout.addWidget(self.path_input, 1)
        main_layout.addWidget(self.browse_button)
        main_layout.addWidget(self.open_button)
        self.setLayout(main_layout)
    def set_field(self, text):
        self.path_input.setText(text)
    def handle_search(self):
        self.search.emit(self.path_input.text())
    def handle_browse(self):
        self.browse.emit()
      
    
class DateSelectWidget(QWidget):
    filtering = Signal(float,float)
    def __init__(self):
        super().__init__()
        self.__init_ui()
    
    def __init_ui(self):
        main_layout = QHBoxLayout()

        self.from_label = QLabel('From', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.from_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.from_date = QDateTimeEdit()
        self.from_date.setDateTime(datetime.now() - timedelta(hours=1))
        self.from_date.setCurrentSection(QDateTimeEdit.HourSection)

        self.to_label = QLabel('To', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.to_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.to_date = QDateTimeEdit()
        self.to_date.setDateTime(datetime.now())
        self.from_date.setCurrentSection(QDateTimeEdit.HourSection)

        self.filter_button = QPushButton('Filter')
        self.filter_button.clicked.connect(self.handle_filtering)

        main_layout.addWidget(self.from_label)
        main_layout.addWidget(self.from_date)
        main_layout.addWidget(self.to_label)
        main_layout.addWidget(self.to_date)
        main_layout.addStretch()
        main_layout.addWidget(self.filter_button)
        self.setLayout(main_layout)

    def handle_filtering(self):
        from_timestamp = self.from_date.dateTime().toSecsSinceEpoch()
        to_timestamp = self.to_date.dateTime().toSecsSinceEpoch()
        self.filtering.emit(from_timestamp, to_timestamp)

    def set_dates(self, begin_timestamp, end_timestamp):
        self.from_date.setDateTime(begin_timestamp)
        self.to_date.setDateTime(end_timestamp)

class LogContentManagerWidget(QWidget):
    next = Signal()
    prev = Signal()
    def __init__(self):
        super().__init__()
        self.__init_ui()
    
    def __init_ui(self):
        main_layout = QHBoxLayout()

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next.emit)
        self.next_button.setEnabled(False)
        self.prev_button = QPushButton('Previous')
        self.prev_button.clicked.connect(self.prev.emit)
        self.prev_button.setEnabled(False)

        main_layout.addWidget(self.prev_button)
        main_layout.addStretch()
        main_layout.addWidget(self.next_button)
        self.setLayout(main_layout)

    def set_enabled_next(self, enabled):
        self.next_button.setEnabled(enabled)

    def set_enabled_prev(self, enabled):
        self.prev_button.setEnabled(enabled)



class LogDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        layout = QFormLayout()  # automatycznie tworzy kolumnę "nazwa - wartość"
        layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignTop)
        layout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.detail_labels = []

        self.detail_row_labels = [
            "Timestamp", "UID", "Host IP", "Host Port", "Server IP", "Server Port", "Trans Depth", "Method", "Host", "URI",
            "Referrer", "User Agent", "Request Body Length", "Response Body Length", "Status Code",
            "Status Message", "Info Code", "Info Message", "Filename", "Tags", "Username",
            "Password", "Proxied", "Orig FUIds", "Orig MIME Types", "Resp FUIds", "Resp MIME Types"]

        for title in self.detail_row_labels:
            label = QLabel("-", wordWrap=True)
            label.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding
            )
            layout.addRow(title + ":", label)
            self.detail_labels.append(label)

        self.setLayout(layout)

    def clear(self):
        for label in self.detail_labels:
            label.setText("-")

    def set_content(self, content):
        for label, value in zip(self.detail_labels, content):
            label.setText(value)


class LogContentWidget(QWidget):
    selected = Signal(str,int,int)
    deselected = Signal()
    def __init__(self):
        super().__init__()
        self.setObjectName('LogContenctWidget')
        self.__init_ui()
    
    def __init_ui(self):
        main_layout = QVBoxLayout()

        self.log_content_widget = QListWidget()
        self.log_content_widget.itemSelectionChanged.connect(self.handle_selection)        
        main_layout.addWidget(self.log_content_widget)
        self.setLayout(main_layout)

    def set_content(self, content):
        for text in content:
            item = QListWidgetItem(text)
            self.log_content_widget.addItem(item)

    def get_content_metrics(self):
        return QFontMetrics(self.log_content_widget.font()), 850


    def handle_selection(self):
        selection = self.log_content_widget.currentItem()
        if selection:
            self.selected.emit(selection.text(),self.log_content_widget.currentRow(), self.log_content_widget.count())
        else:
            self.deselected.emit()

    def next(self):
        current = self.log_content_widget.currentRow()
        if current < self.log_content_widget.count() - 1:
            self.log_content_widget.setCurrentRow(current + 1)
        self.handle_selection()

    def prev(self):
        current = self.log_content_widget.currentRow()
        if current > 0:
            self.log_content_widget.setCurrentRow(current - 1)
        self.handle_selection()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet("""
    QWidget {
        font-family: 'Segoe UI';
        font-size: 12px;
    },
""")


    window = MainWindow()
    window.show()
    app.exec()
