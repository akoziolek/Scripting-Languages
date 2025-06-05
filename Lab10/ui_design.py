# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_project.ui'
# Created by: PyQt5 UI code generator 5.15.11
# WARNING: Manual changes will be lost when pyuic5 is run again.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # ===== Main Window Configuration =====
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(915, 514)
        MainWindow.setMinimumSize(QtCore.QSize(915, 514))

        # Font settings
        main_font = QtGui.QFont()
        main_font.setPointSize(9)
        MainWindow.setFont(main_font)

        # Window behavior
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)

        # ===== Central Widget and Main Layout =====
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_vertical_layout.setObjectName("main_vertical_layout")

        # ===== File Path Section =====
        self.file_path_layout = QtWidgets.QHBoxLayout()
        self.file_path_layout.setObjectName("file_path_layout")

        # File path input
        self.lineEdit_file_path = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_file_path.setAutoFillBackground(False)
        self.lineEdit_file_path.setText("")
        self.lineEdit_file_path.setClearButtonEnabled(True)
        self.file_path_layout.addWidget(self.lineEdit_file_path)

        # Browse button
        self.pushButton_browse = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_browse.setFixedWidth(22)
        self.file_path_layout.addWidget(self.pushButton_browse)

        # Search button
        self.pushButton_search = QtWidgets.QPushButton(self.centralwidget)
        self.file_path_layout.addWidget(self.pushButton_search)

        # Stretch factors
        self.file_path_layout.setStretch(0, 5)  # Path input gets most space
        self.file_path_layout.setStretch(1, 1)  # Browse button
        self.file_path_layout.setStretch(2, 1)  # Search button

        self.main_vertical_layout.addLayout(self.file_path_layout)

        # Horizontal divider line
        self.divider_line_1 = self._create_horizontal_divider()
        self.main_vertical_layout.addWidget(self.divider_line_1)

        # ===== Main Content Grid =====
        self.main_grid_layout = QtWidgets.QGridLayout()
        self.main_grid_layout.setObjectName("main_grid_layout")

        # ===== Table Selection Section =====
        self.label_choice = QtWidgets.QLabel(self.centralwidget)
        self._set_bold_font(self.label_choice)
        self.main_grid_layout.addWidget(self.label_choice, 0, 0, 1, 1)

        self.comboBox_table = QtWidgets.QComboBox(self.centralwidget)
        self.main_grid_layout.addWidget(self.comboBox_table, 0, 1, 1, 1)

        # Navigation buttons
        self.pushButton_prev = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_prev.setMaximumWidth(91)
        self.main_grid_layout.addWidget(self.pushButton_prev, 3, 0, 1, 1)

        self.pushButton_next = QtWidgets.QPushButton(self.centralwidget)
        self.main_grid_layout.addWidget(self.pushButton_next, 3, 6, 1, 1)

        # Page navigation
        self.pushButton_prev_page = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_prev_page.setFixedWidth(22)
        self.main_grid_layout.addWidget(self.pushButton_prev_page, 3, 2, 1, 1)

        self.label_page = QtWidgets.QLabel(self.centralwidget)
        self.main_grid_layout.addWidget(self.label_page, 3, 3, 1, 1)

        self.pushButton_next_page = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_next_page.setFixedWidth(22)
        self.main_grid_layout.addWidget(self.pushButton_next_page, 3, 4, 1, 1)

        # Spacers
        self.main_grid_layout.addItem(
            QtWidgets.QSpacerItem(188, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            3, 1, 1, 1
        )
        self.main_grid_layout.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            3, 5, 1, 1
        )

        # ===== Data Table =====
        self.tableWidget_records = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_records.setColumnCount(0)
        self.tableWidget_records.setRowCount(0)
        self.main_grid_layout.addWidget(self.tableWidget_records, 2, 0, 1, 7)

        # Column stretch
        self.main_grid_layout.setColumnStretch(0, 1)

        # ===== Statistics Panel =====
        self.label_stats = QtWidgets.QLabel(self.centralwidget)
        self._set_bold_font(self.label_stats)
        self.main_grid_layout.addWidget(self.label_stats, 0, 7, 1, 1)

        self.stats_panel = self._create_stats_panel()
        self.main_grid_layout.addLayout(self.stats_panel, 2, 7, 1, 1)

        self.main_vertical_layout.addLayout(self.main_grid_layout)

        # Final divider line
        self.divider_line_2 = self._create_horizontal_divider()
        self.main_vertical_layout.addWidget(self.divider_line_2)

        # ===== Status Bar =====
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # Final setup
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _create_horizontal_divider(self):
        """Helper to create consistent divider lines"""
        line = QtWidgets.QFrame(self.centralwidget)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        return line

    def _set_bold_font(self, widget):
        """Helper to apply bold font to labels"""
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        widget.setFont(font)

    def _create_stats_panel(self):
        """Creates the statistics panel with all metrics"""
        stats_layout = QtWidgets.QVBoxLayout()

        # Statistic 1: Average rental duration
        stats_layout.addWidget(self._create_horizontal_divider())
        self.label_stat1 = QtWidgets.QLabel(self.centralwidget)
        self.label_stat1.setWordWrap(True)
        stats_layout.addWidget(self.label_stat1)

        self.label_stat1_res = QtWidgets.QLabel(self.centralwidget)
        self.label_stat1_res.setWordWrap(True)
        stats_layout.addWidget(self.label_stat1_res)

        # Statistic 2: Average return duration
        stats_layout.addWidget(self._create_horizontal_divider())
        self.label_stat2 = QtWidgets.QLabel(self.centralwidget)
        self.label_stat2.setWordWrap(True)
        stats_layout.addWidget(self.label_stat2)

        self.label_stat2_res = QtWidgets.QLabel(self.centralwidget)
        self.label_stat2_res.setWordWrap(True)
        stats_layout.addWidget(self.label_stat2_res)

        # Statistic 3: Different bikes count
        stats_layout.addWidget(self._create_horizontal_divider())
        self.label_stat3 = QtWidgets.QLabel(self.centralwidget)
        self.label_stat3.setWordWrap(True)
        stats_layout.addWidget(self.label_stat3)

        self.label_stat3_res = QtWidgets.QLabel(self.centralwidget)
        self.label_stat3_res.setWordWrap(True)
        stats_layout.addWidget(self.label_stat3_res)

        # Statistic 4: Custom metric
        stats_layout.addWidget(self._create_horizontal_divider())
        self.label_stat4 = QtWidgets.QLabel(self.centralwidget)
        self.label_stat4.setWordWrap(True)
        stats_layout.addWidget(self.label_stat4)

        self.label_stat4_res = QtWidgets.QLabel(self.centralwidget)
        self.label_stat4_res.setWordWrap(True)
        stats_layout.addWidget(self.label_stat4_res)

        # Final divider and spacer
        stats_layout.addWidget(self._create_horizontal_divider())
        stats_layout.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        )

        return stats_layout

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Baza danych przejazdów rowerowych"))

        # File section
        self.lineEdit_file_path.setPlaceholderText(_translate("MainWindow", "C:\\Sciezka_do_bazy_danych"))
        self.pushButton_browse.setText(_translate("MainWindow", "..."))
        self.pushButton_search.setText(_translate("MainWindow", "Szukaj"))

        # Table section
        self.label_choice.setText(_translate("MainWindow", "Wybrana tabela:"))
        self.pushButton_prev.setText(_translate("MainWindow", "Poprzedni"))
        self.pushButton_next.setText(_translate("MainWindow", "Następny"))
        self.label_page.setText(_translate("MainWindow", "0 z 0"))
        self.pushButton_next_page.setText(_translate("MainWindow", ">>"))
        self.pushButton_prev_page.setText(_translate("MainWindow", "<<"))

        # Statistics section
        self.label_stats.setText(_translate("MainWindow", "Statystyki:"))
        self.label_stat1.setText(_translate("MainWindow", "Średni czas trwania przejazdu rozpoczynanego na stacji: "))
        self.label_stat1_res.setText(_translate("MainWindow", "2132,12"))
        self.label_stat2.setText(_translate("MainWindow", "Średni czas trwania przejazdu kończonego na stacji: "))
        self.label_stat2_res.setText(_translate("MainWindow", "4212"))
        self.label_stat3.setText(_translate("MainWindow", "Liczba różnych rowerów parkowanych na danej stacji:"))
        self.label_stat3_res.setText(_translate("MainWindow", "0"))
        self.label_stat4.setText(_translate("MainWindow", "Niespodzianka: ?"))
        self.label_stat4_res.setText(_translate("MainWindow", "6546"))