import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QFileDialog, QListWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from md5_hashing import md5_string, md5_file, integrity_check
from folderIntegrityCheck import compare_hash_files
from hashingFunctions import *

class MD5HasherApp(QWidget):
    def __init__(self):
        super().__init__()

        # Загрузка и применение таблицы стилей
        with open('styles.css', 'r') as file:
            self.setStyleSheet(file.read())
            

        self.setWindowTitle('MD5 Хеширование')
        self.setGeometry(100, 100, 800, 600)  # Увеличенный размер окна

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)  # Увеличенные отступы
        self.layout.setSpacing(15)  # Увеличенное расстояние

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)  # Современный стиль вкладок
        self.layout.addWidget(self.tabs)

        # Добавление отступов между секциями
        def add_spacing(layout):
            spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            layout.addItem(spacer)

        # Вкладка 1: Хеширование строки
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.tab1_layout.setContentsMargins(20, 20, 20, 20)
        self.tab1_layout.setSpacing(15)

        self.input_label = QLabel('Введите строку:')
        self.input_label.setFont(QFont('Arial', 12))
        self.tab1_layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        self.input_field.setFont(QFont('Arial', 12))
        self.input_field.textChanged.connect(self.update_hash_realtime)
        self.tab1_layout.addWidget(self.input_field)

        self.hash_label = QLabel('MD5 Хеш:')
        self.hash_label.setFont(QFont('Arial', 12))
        self.tab1_layout.addWidget(self.hash_label)

        self.hash_output = QLineEdit()
        self.hash_output.setFont(QFont('Arial', 12))
        self.hash_output.setReadOnly(True)
        self.tab1_layout.addWidget(self.hash_output)

        # Эталонный хеш для сравнения
        self.reference_hash_label = QLabel('Эталонный хеш:')
        self.reference_hash_label.setFont(QFont('Arial', 12))
        self.tab1_layout.addWidget(self.reference_hash_label)

        self.reference_hash_input = QLineEdit()
        self.reference_hash_input.setFont(QFont('Arial', 12))
        self.tab1_layout.addWidget(self.reference_hash_input)

        self.check_button = QPushButton('Проверить хеш')
        self.check_button.setFont(QFont('Arial', 12))
        self.check_button.clicked.connect(self.check_hash_string)
        self.tab1_layout.addWidget(self.check_button)

        self.result_label = QLabel('Результат проверки:')
        self.result_label.setFont(QFont('Arial', 12))
        self.tab1_layout.addWidget(self.result_label)

        self.result_output = QLabel('')
        self.result_output.setFont(QFont('Arial', 12))
        self.tab1_layout.addWidget(self.result_output)

        add_spacing(self.tab1_layout)  # Добавить отступы между секциями

        self.tab1.setLayout(self.tab1_layout)
        self.tabs.addTab(self.tab1, 'Хеширование строки')

        # Вкладка 2: Хеширование файла
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.setContentsMargins(20, 20, 20, 20)
        self.tab2_layout.setSpacing(15)

        self.file_label = QLabel('Выберите файл для хеширования:')
        self.file_label.setFont(QFont('Arial', 12))
        self.tab2_layout.addWidget(self.file_label)

        self.file_button = QPushButton('Выбрать файл')
        self.file_button.setFont(QFont('Arial', 12))
        self.file_button.clicked.connect(self.on_file_button_click)
        self.tab2_layout.addWidget(self.file_button)

        self.hash_label_file = QLabel('MD5 Хеш:')
        self.hash_label_file.setFont(QFont('Arial', 12))
        self.tab2_layout.addWidget(self.hash_label_file)

        self.hash_output_file = QLineEdit()
        self.hash_output_file.setFont(QFont('Arial', 12))
        self.hash_output_file.setReadOnly(True)
        self.tab2_layout.addWidget(self.hash_output_file)

        # Эталонный хеш для сравнения
        self.reference_hash_label_file = QLabel('Эталонный хеш:')
        self.reference_hash_label_file.setFont(QFont('Arial', 12))
        self.tab2_layout.addWidget(self.reference_hash_label_file)

        self.reference_hash_input_file = QLineEdit()
        self.reference_hash_input_file.setFont(QFont('Arial', 12))
        self.tab2_layout.addWidget(self.reference_hash_input_file)

        self.check_button_file = QPushButton('Проверить хеш')
        self.check_button_file.setFont(QFont('Arial', 12))
        self.check_button_file.clicked.connect(self.check_hash_file)
        self.tab2_layout.addWidget(self.check_button_file)

        self.result_label_file = QLabel('Результат проверки:')
        self.result_label_file.setFont(QFont('Arial', 12))
        self.tab2_layout.addWidget(self.result_label_file)

        self.result_output_file = QLabel('')
        self.result_output_file.setFont(QFont('Arial', 12))
        self.tab2_layout.addWidget(self.result_output_file)

        add_spacing(self.tab2_layout)  # Добавить отступы между секциями

        self.tab2.setLayout(self.tab2_layout)
        self.tabs.addTab(self.tab2, 'Хеширование файла')

        # Вкладка 3: Хеширование файлов в папке и сравнение хешей
        self.tab3 = QWidget()
        self.tab3_layout = QVBoxLayout()
        self.tab3_layout.setContentsMargins(20, 20, 20, 20)
        self.tab3_layout.setSpacing(15)

        self.folder_label = QLabel('Выберите папку для хеширования файлов:')
        self.folder_label.setFont(QFont('Arial', 12))
        self.tab3_layout.addWidget(self.folder_label)

        self.folder_button = QPushButton('Выбрать папку')
        self.folder_button.setFont(QFont('Arial', 12))
        self.folder_button.clicked.connect(self.on_folder_button_click)
        self.tab3_layout.addWidget(self.folder_button)

        self.files_list = QListWidget()
        self.files_list.setFont(QFont('Arial', 12))
        self.tab3_layout.addWidget(self.files_list)

        self.compare_label = QLabel('Сравнение файлов с хешами:')
        self.compare_label.setFont(QFont('Arial', 12))
        self.tab3_layout.addWidget(self.compare_label)

        self.select_ref_button = QPushButton('Выбрать эталонный файл')
        self.select_ref_button.setFont(QFont('Arial', 12))
        self.select_ref_button.clicked.connect(self.select_reference_file)
        self.tab3_layout.addWidget(self.select_ref_button)

        self.select_curr_button = QPushButton('Выбрать текущий файл')
        self.select_curr_button.setFont(QFont('Arial', 12))
        self.select_curr_button.clicked.connect(self.select_current_file)
        self.tab3_layout.addWidget(self.select_curr_button)

        self.compare_button = QPushButton('Сравнить файлы')
        self.compare_button.setFont(QFont('Arial', 12))
        self.compare_button.clicked.connect(self.compare_files)
        self.tab3_layout.addWidget(self.compare_button)

        self.compare_results = QListWidget()
        self.compare_results.setFont(QFont('Arial', 12))
        self.tab3_layout.addWidget(self.compare_results)

        add_spacing(self.tab3_layout)  # Добавить отступы между секциями

        self.tab3.setLayout(self.tab3_layout)
        self.tabs.addTab(self.tab3, 'Хеширование и сравнение')

        # Добавить Вкладку 4: Хеш папки
        self.tab4 = QWidget()
        self.tab4_layout = QVBoxLayout()
        self.tab4_layout.setContentsMargins(20, 20, 20, 20)
        self.tab4_layout.setSpacing(15)

        self.folder_hash_label = QLabel('Выберите папку для вычисления общего хеша:')
        self.folder_hash_label.setFont(QFont('Arial', 12))
        self.tab4_layout.addWidget(self.folder_hash_label)

        self.folder_hash_button = QPushButton('Выбрать папку')
        self.folder_hash_button.setFont(QFont('Arial', 12))
        self.folder_hash_button.clicked.connect(self.calculate_folder_hash)
        self.folder_hash_button.setMinimumHeight(40)
        self.tab4_layout.addWidget(self.folder_hash_button)

        self.folder_hash_output_label = QLabel('Общий хеш папки:')
        self.folder_hash_output_label.setFont(QFont('Arial', 12))
        self.tab4_layout.addWidget(self.folder_hash_output_label)

        self.folder_hash_output = QLineEdit()
        self.folder_hash_output.setFont(QFont('Arial', 12))
        self.folder_hash_output.setReadOnly(True)
        self.folder_hash_output.setMinimumHeight(40)
        self.tab4_layout.addWidget(self.folder_hash_output)

        self.folder_reference_hash_label = QLabel('Эталонный хеш папки:')
        self.folder_reference_hash_label.setFont(QFont('Arial', 12))
        self.tab4_layout.addWidget(self.folder_reference_hash_label)

        self.folder_reference_hash_input = QLineEdit()
        self.folder_reference_hash_input.setFont(QFont('Arial', 12))
        self.folder_reference_hash_input.setMinimumHeight(40)
        self.tab4_layout.addWidget(self.folder_reference_hash_input)

        self.folder_check_button = QPushButton('Проверить хеш')
        self.folder_check_button.setFont(QFont('Arial', 12))
        self.folder_check_button.clicked.connect(self.check_folder_hash)
        self.folder_check_button.setMinimumHeight(40)
        self.tab4_layout.addWidget(self.folder_check_button)

        self.folder_result_label = QLabel('Результат проверки:')
        self.folder_result_label.setFont(QFont('Arial', 12))
        self.tab4_layout.addWidget(self.folder_result_label)

        self.folder_result_output = QLabel('')
        self.folder_result_output.setFont(QFont('Arial', 12))
        self.tab4_layout.addWidget(self.folder_result_output)

        self.tab4.setLayout(self.tab4_layout)
        self.tabs.addTab(self.tab4, 'Хеш папки')

        self.setLayout(self.layout)

        # Атрибуты для хранения путей к файлам
        self.reference_file_path = None
        self.current_file_path = None

        # Установка фиксированной высоты для кнопок
        for button in self.findChildren(QPushButton):
            button.setMinimumHeight(40)

        # Установка фиксированной высоты для полей ввода
        for input_field in self.findChildren(QLineEdit):
            input_field.setMinimumHeight(40)

    def update_hash_realtime(self, text):
        update_hash_realtime(text, self.hash_output)

    def check_hash_string(self):
        check_hash_string(self.hash_output, self.reference_hash_input, self.result_output)

    def on_file_button_click(self):
        on_file_button_click(self, self.hash_output_file)

    def check_hash_file(self):
        check_hash_file(self.hash_output_file, self.reference_hash_input_file, self.result_output_file)

    def on_folder_button_click(self):
        on_folder_button_click(self, self.files_list)

    def select_reference_file(self):
        self.reference_file_path = select_reference_file(self, self.compare_results)

    def select_current_file(self):
        self.current_file_path = select_current_file(self, self.compare_results)

    def compare_files(self):
        compare_files(self.reference_file_path, self.current_file_path, self.compare_results)

    def calculate_folder_hash(self):
        calculate_folder_hash(self, self.folder_hash_output)

    def check_folder_hash(self):
        check_folder_hash(self.folder_hash_output.text(), 
                         self.folder_reference_hash_input.text(), 
                         self.folder_result_output)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MD5HasherApp()
    window.show()
    sys.exit(app.exec())
