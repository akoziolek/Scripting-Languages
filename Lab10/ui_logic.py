import os
import sys
from math import ceil

from PyQt5.QtCore import QtWarningMsg
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem

from Lab10 import select_sqlalchemy
from ui_design import Ui_MainWindow
import select_SQLite

page_size = 9

class MainWindow(QMainWindow):
    def __init__(self, db_type = 'SQLite'):
        self.current_page = 0
        self.records = None
        self.module = select_SQLite if db_type == 'SQLite' else select_sqlalchemy
        super().__init__()
        self.db_type = db_type
        self.station_map = {}

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.setFixedSize(1600, 900)
        self.ui.setupUi(self)


        self.ui.pushButton_browse.clicked.connect(self.handle_browse)
        self.ui.pushButton_search.clicked.connect(self.handle_search)
        self.ui.lineEdit_file_path.returnPressed.connect(self.handle_search)
        self.ui.comboBox_station.currentIndexChanged.connect(self.refresh_table_data)
        self.ui.pushButton_next_page.clicked.connect(self.next_page)
        self.ui.pushButton_prev_page.clicked.connect(self.prev_page)
        self.selected_index = 0  # absolute record index
        self.ui.pushButton_next.clicked.connect(self.handle_next_record)
        self.ui.pushButton_prev.clicked.connect(self.handle_prev_record)
        self.ui.tableWidget_records.itemSelectionChanged.connect(self.handle_row_selection)

        # Show the window
        self.show()

    def next_page(self):
        self.current_page += 1
        self.refresh_table_view()
        self.handle_row_selection()

    def prev_page(self):
        self.current_page -= 1
        self.refresh_table_view()
        self.handle_row_selection()

    def handle_browse(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            os.getcwd(),
            "SQLite (*.sqlite3 *.db)"
        )
        self.ui.lineEdit_file_path.setText(file_path)
        self.handle_search()

    def handle_search(self):
        file_path = self.ui.lineEdit_file_path.text()
        if file_path:
            try:
                self.refresh_stations()
            except Exception as e:
                QMessageBox.warning(
                    self,
                    'Error',
                    str(e),
                    QMessageBox.Ok
                )

    def refresh_pages(self):
        self.ui.label_page.setText(f'{self.current_page} z {ceil(len(self.records) / page_size)}')

    def refresh_stations(self):
        file_path = self.ui.lineEdit_file_path.text()
        self.station_map = dict(self.module.get_all_stations(file_path))
        self.ui.comboBox_station.clear()
        self.ui.comboBox_station.addItems(self.module.get_all_station_names(file_path))
        self.refresh_table_data()

    def refresh_table_data(self):
        file_path = self.ui.lineEdit_file_path.text()
        station_id = self.station_map[self.ui.comboBox_station.currentText()]

        avg_rental = self.module.average_duration_rental_stat(file_path, station_id)
        avg_return = self.module.average_duration_return_stat(file_path, station_id)
        distinct_bikes = self.module.num_of_diff_bikes(file_path, station_id)
        common_station = self.module.most_common_return_station(file_path, station_id)

        self.ui.label_stat1_res.setText(f"{avg_rental if avg_rental is not None else 'N/A'} min")
        self.ui.label_stat2_res.setText(f"{avg_return if avg_return is not None else 'N/A'} min")
        self.ui.label_stat3_res.setText(f"{distinct_bikes if distinct_bikes is not None else 'N/A'}")
        self.ui.label_stat4_res.setText(f"{common_station if common_station is not None else 'N/A'}")

        data = self.module.logs_by_station(file_path, self.ui.comboBox_station.currentText())
        self.records = data
        self.current_page = 1
        self.refresh_table_view()

    def refresh_table_view(self):
        data = self.records
        self.ui.pushButton_next_page.setEnabled(self.current_page < ceil(len(self.records) / page_size))
        self.ui.pushButton_prev_page.setEnabled(self.current_page > 1)
        
        self.ui.tableWidget_records.clear()
        start = (self.current_page - 1) * page_size
        end = min(len(data), self.current_page * page_size)
        self.ui.tableWidget_records.setRowCount(end - start)
        self.ui.tableWidget_records.setColumnCount(len(data[0]) if data else 0)

        
        for rel_row_idx, row_idx in enumerate(range(start, end)):
            row_data = self.records[row_idx]
            for col_idx, cell_data in enumerate(row_data):
                self.ui.tableWidget_records.setItem(rel_row_idx, col_idx, QTableWidgetItem(str(cell_data)))

        
        self.ui.tableWidget_records.setHorizontalHeaderLabels(
            ['id', 'bike id', 'start time', 'stop time', 'start station', 'stop station']
        )

        self.refresh_pages()

    def handle_next_record(self):
        if not self.records:
            return

        if self.selected_index < len(self.records) - 1:
            self.selected_index += 1
            new_page = self.selected_index // page_size + 1
            if new_page != self.current_page:
                self.current_page = new_page
                self.refresh_table_view()
                self.highlight_selected_row()
            else:
                self.highlight_selected_row()

    def highlight_selected_row(self):
        page_start_index = (self.current_page - 1) * page_size
        local_row_index = self.selected_index - page_start_index

        self.ui.tableWidget_records.clearSelection()
        self.ui.tableWidget_records.selectRow(local_row_index)
        self.ui.tableWidget_records.scrollToItem(self.ui.tableWidget_records.item(local_row_index, 0))

    def handle_prev_record(self):
        if not self.records:
            return

        if self.selected_index > 0:
            self.selected_index -= 1
            new_page = self.selected_index // page_size + 1
            if new_page != self.current_page:
                self.current_page = new_page
                self.refresh_table_view()
                self.highlight_selected_row()
            else:
                self.highlight_selected_row()

    def handle_row_selection(self):
        self.ui.pushButton_next.setEnabled(self.selected_index < len(self.records) - 1)
        self.ui.pushButton_prev.setEnabled(self.selected_index > 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow('sqlalchemy')
    sys.exit(app.exec_())