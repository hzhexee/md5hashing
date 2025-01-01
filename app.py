import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QFileDialog, QListWidget
from PyQt6.QtCore import Qt
from md5_hashing import md5_string, md5_file, integrity_check
from folderIntegrityCheck import compare_hash_files

class MD5HasherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MD5 Хеширование')
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Вкладка 1: Хеширование строки
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()

        self.input_label = QLabel('Введите строку:')
        self.tab1_layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        self.input_field.textChanged.connect(self.update_hash_realtime)
        self.tab1_layout.addWidget(self.input_field)

        self.hash_label = QLabel('MD5 Хеш:')
        self.tab1_layout.addWidget(self.hash_label)

        self.hash_output = QLineEdit()
        self.hash_output.setReadOnly(True)
        self.tab1_layout.addWidget(self.hash_output)

        # Эталонный хеш для сравнения
        self.reference_hash_label = QLabel('Эталонный хеш:')
        self.tab1_layout.addWidget(self.reference_hash_label)

        self.reference_hash_input = QLineEdit()
        self.tab1_layout.addWidget(self.reference_hash_input)

        self.check_button = QPushButton('Проверить хеш')
        self.check_button.clicked.connect(self.check_hash_string)
        self.tab1_layout.addWidget(self.check_button)

        self.result_label = QLabel('Результат проверки:')
        self.tab1_layout.addWidget(self.result_label)

        self.result_output = QLabel('')
        self.tab1_layout.addWidget(self.result_output)

        self.tab1.setLayout(self.tab1_layout)
        self.tabs.addTab(self.tab1, 'Хеширование строки')

        # Вкладка 2: Хеширование файла
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()

        self.file_label = QLabel('Выберите файл для хеширования:')
        self.tab2_layout.addWidget(self.file_label)

        self.file_button = QPushButton('Выбрать файл')
        self.file_button.clicked.connect(self.on_file_button_click)
        self.tab2_layout.addWidget(self.file_button)

        self.hash_label_file = QLabel('MD5 Хеш:')
        self.tab2_layout.addWidget(self.hash_label_file)

        self.hash_output_file = QLineEdit()
        self.hash_output_file.setReadOnly(True)
        self.tab2_layout.addWidget(self.hash_output_file)

        # Эталонный хеш для сравнения
        self.reference_hash_label_file = QLabel('Эталонный хеш:')
        self.tab2_layout.addWidget(self.reference_hash_label_file)

        self.reference_hash_input_file = QLineEdit()
        self.tab2_layout.addWidget(self.reference_hash_input_file)

        self.check_button_file = QPushButton('Проверить хеш')
        self.check_button_file.clicked.connect(self.check_hash_file)
        self.tab2_layout.addWidget(self.check_button_file)

        self.result_label_file = QLabel('Результат проверки:')
        self.tab2_layout.addWidget(self.result_label_file)

        self.result_output_file = QLabel('')
        self.tab2_layout.addWidget(self.result_output_file)

        self.tab2.setLayout(self.tab2_layout)
        self.tabs.addTab(self.tab2, 'Хеширование файла')

        # Вкладка 3: Хеширование файлов в папке и сравнение хешей
        self.tab3 = QWidget()
        self.tab3_layout = QVBoxLayout()

        self.folder_label = QLabel('Выберите папку для хеширования файлов:')
        self.tab3_layout.addWidget(self.folder_label)

        self.folder_button = QPushButton('Выбрать папку')
        self.folder_button.clicked.connect(self.on_folder_button_click)
        self.tab3_layout.addWidget(self.folder_button)

        self.files_list = QListWidget()
        self.tab3_layout.addWidget(self.files_list)

        self.compare_label = QLabel('Сравнение файлов с хешами:')
        self.tab3_layout.addWidget(self.compare_label)

        self.select_ref_button = QPushButton('Выбрать эталонный файл')
        self.select_ref_button.clicked.connect(self.select_reference_file)
        self.tab3_layout.addWidget(self.select_ref_button)

        self.select_curr_button = QPushButton('Выбрать текущий файл')
        self.select_curr_button.clicked.connect(self.select_current_file)
        self.tab3_layout.addWidget(self.select_curr_button)

        self.compare_button = QPushButton('Сравнить файлы')
        self.compare_button.clicked.connect(self.compare_files)
        self.tab3_layout.addWidget(self.compare_button)

        self.compare_results = QListWidget()
        self.tab3_layout.addWidget(self.compare_results)

        self.tab3.setLayout(self.tab3_layout)
        self.tabs.addTab(self.tab3, 'Хеширование и сравнение')

        self.setLayout(self.layout)

        # Атрибуты для хранения путей к файлам
        self.reference_file_path = None
        self.current_file_path = None

    def update_hash_realtime(self, text):
        if text:
            hashed_text = md5_string(text)
            self.hash_output.setText(hashed_text)
        else:
            self.hash_output.clear()

    def check_hash_string(self):
        # Получаем значения из полей
        hash1 = self.hash_output.text()
        hash2 = self.reference_hash_input.text()

        # Проверяем хеши
        if integrity_check(hash1, hash2):
            self.result_output.setText('Хеши совпадают!')
        else:
            self.result_output.setText('Хеши не совпадают!')

    def on_file_button_click(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл для хеширования", "", "Все файлы (*)")
        if file_path:
            hashed_text = md5_file(file_path)
            self.hash_output_file.setText(hashed_text)
        else:
            self.hash_output_file.clear()

    def check_hash_file(self):
        # Получаем значения из полей
        hash1 = self.hash_output_file.text()
        hash2 = self.reference_hash_input_file.text()

        # Проверяем хеши
        if integrity_check(hash1, hash2):
            self.result_output_file.setText('Хеши совпадают!')
        else:
            self.result_output_file.setText('Хеши не совпадают!')

    def on_folder_button_click(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для хеширования файлов")
        if folder_path:
            self.files_list.clear()

            output_file_path = os.path.join(folder_path, "file_hashes.txt")

            with open(output_file_path, "w") as output_file:
                output_file.write("Файл\tMD5 Хеш\n")

                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        hashed_text = md5_file(file_path)

                        self.files_list.addItem(f"{file}: {hashed_text}")
                        output_file.write(f"{file}: {hashed_text}\n")

            self.files_list.addItem(f"\nХеши файлов сохранены в {output_file_path}")

    def select_reference_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите эталонный файл с хешами", "", "Все файлы (*)")
        if file_path:
            self.reference_file_path = file_path
            self.compare_results.addItem(f"Эталонный файл выбран: {file_path}")

    def select_current_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите текущий файл с хешами", "", "Все файлы (*)")
        if file_path:
            self.current_file_path = file_path
            self.compare_results.addItem(f"Текущий файл выбран: {file_path}")

    def compare_files(self):
        if not self.reference_file_path or not self.current_file_path:
            self.compare_results.addItem("Ошибка: Не выбраны оба файла для сравнения.")
            return

        result = compare_hash_files(self.reference_file_path, self.current_file_path)

        self.compare_results.clear()
        self.compare_results.addItem("Совпадающие файлы:")
        self.compare_results.addItems(result["matched"] or ["Нет совпадений"])
        self.compare_results.addItem("\nНесовпадающие файлы:")
        self.compare_results.addItems(result["mismatched"] or ["Нет несовпадений"])
        self.compare_results.addItem("\nОтсутствующие файлы:")
        self.compare_results.addItems(result["missing"] or ["Нет отсутствующих файлов"])

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MD5HasherApp()
    window.show()
    sys.exit(app.exec())
