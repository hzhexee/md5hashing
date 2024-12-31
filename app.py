import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QFileDialog
from PyQt6.QtCore import Qt
from md5_hashing import md5_string, md5_file, integrity_check

class MD5HasherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MD5 Хеширование')
        self.setGeometry(100, 100, 400, 350)

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

        self.setLayout(self.layout)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MD5HasherApp()
    window.show()
    sys.exit(app.exec())
