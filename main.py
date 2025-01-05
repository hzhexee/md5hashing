import sys
from PyQt6.QtWidgets import QApplication, QWidget
from md5_hasher_ui import Ui_MD5HasherApp
from md5_gui_handlers import *
from md5_core import MD5StepByStep

class MD5HasherApp(QWidget):
    """
    Главное приложение для MD5 хеширования с графическим интерфейсом.
    
    Предоставляет функциональность для:
    - Хеширования строк
    - Хеширования файлов
    - Сравнения файлов
    - Хеширования папок
    - Визуализации процесса MD5 хеширования
    """

    def __init__(self):
        """Инициализирует приложение и настраивает пользовательский интерфейс."""
        super().__init__()
        
        # Инициализация пользовательского интерфейса
        self.ui = Ui_MD5HasherApp()
        self.ui.setupUi(self)
        
        # Установка минимального и максимального размера окна
        self.setMinimumSize(1000, 800)
        self.setMaximumSize(1000, 800)

        # Загрузка и применение стиля
        with open('md5_gui_styles.css', 'r') as file:
            self.setStyleSheet(file.read())

        # Сохранение путей к файлам для сравнения
        self.reference_file_path = None
        self.current_file_path = None

        self.md5_stepper = None

        # Подключение сигналов и слотов
        self.setup_connections()

    def setup_connections(self):
        """
        Устанавливает связи между сигналами и слотами для всех элементов интерфейса.
        
        Подключает все кнопки и поля ввода к соответствующим обработчикам событий.
        """
        # Tab 1: String hashing
        self.ui.input_field.textChanged.connect(self.update_hash_realtime)
        self.ui.check_button.clicked.connect(self.check_hash_string)

        # Tab 2: File hashing
        self.ui.file_button.clicked.connect(self.on_file_button_click)
        self.ui.check_button_file.clicked.connect(self.check_hash_file)

        # Tab 3: Folder hashing and comparison
        self.ui.folder_button.clicked.connect(self.on_folder_button_click)
        self.ui.select_ref_button.clicked.connect(self.select_reference_file)
        self.ui.select_curr_button.clicked.connect(self.select_current_file)
        self.ui.compare_button.clicked.connect(self.compare_files)

        # Tab 4: Folder hash
        self.ui.folder_hash_button.clicked.connect(self.calculate_folder_hash)
        self.ui.folder_check_button.clicked.connect(self.check_folder_hash)

        # Tab 5: MD5 Visualization
        self.ui.viz_start_button.clicked.connect(self.start_visualization)
        self.ui.viz_next_button.clicked.connect(self.next_visualization_step)

    # Handler methods that connect to the existing handler functions
    def update_hash_realtime(self, text):
        """
        Обновляет хеш в реальном времени при изменении входного текста.
        
        Args:
            text (str): Текущий текст в поле ввода
        """
        update_hash_realtime(text, self.ui.hash_output)

    def check_hash_string(self):
        """
        Проверяет соответствие вычисленного хеша с введенным эталонным значением.
        """
        check_hash_string(self.ui.hash_output, self.ui.reference_hash_input, self.ui.result_output)

    def on_file_button_click(self):
        """
        Обрабатывает нажатие кнопки выбора файла.
        Открывает диалог выбора файла и вычисляет его хеш.
        """
        on_file_button_click(self, self.ui.hash_output_file)

    def check_hash_file(self):
        """
        Проверяет соответствие хеша файла с введенным эталонным значением.
        """
        check_hash_file(self.ui.hash_output_file, self.ui.reference_hash_input_file, self.ui.result_output_file)

    def on_folder_button_click(self):
        """
        Обрабатывает нажатие кнопки выбора папки.
        Открывает диалог выбора папки и отображает список файлов.
        """
        on_folder_button_click(self, self.ui.files_list)

    def select_reference_file(self):
        """
        Выбирает эталонный файл для сравнения.
        
        Returns:
            str: Путь к выбранному файлу
        """
        self.reference_file_path = select_reference_file(self, self.ui.compare_results)

    def select_current_file(self):
        """
        Выбирает текущий файл для сравнения.
        
        Returns:
            str: Путь к выбранному файлу
        """
        self.current_file_path = select_current_file(self, self.ui.compare_results)

    def compare_files(self):
        """
        Сравнивает MD5 хеши эталонного и текущего файлов.
        Отображает результат сравнения в интерфейсе.
        """
        compare_files(self.reference_file_path, self.current_file_path, self.ui.compare_results)

    def calculate_folder_hash(self):
        """
        Вычисляет MD5 хеш для всех файлов в выбранной папке.
        Отображает результат в интерфейсе.
        """
        calculate_folder_hash(self, self.ui.folder_hash_output)

    def check_folder_hash(self):
        """
        Проверяет соответствие вычисленного хеша папки с эталонным значением.
        """
        check_folder_hash(
            self.ui.folder_hash_output.text(),
            self.ui.folder_reference_hash_input.text(),
            self.ui.folder_result_output
        )

    def start_visualization(self):
        """
        Начинает пошаговую визуализацию процесса MD5 хеширования.
        Инициализирует MD5StepByStep для введенного текста.
        """
        input_text = self.ui.viz_input.text()
        if not input_text:
            self.ui.viz_output.clear()
            return
            
        try:
            self.md5_stepper = MD5StepByStep(bytearray(input_text, 'utf-8'))
            self.ui.viz_next_button.setEnabled(True)
            self.ui.viz_output.clear()
            self.ui.viz_output.append("Процесс хеширования начат. Нажмите 'Следующий шаг', чтобы продолжить.")
        except Exception as e:
            self.ui.viz_output.append(f"Ошибка: {str(e)}")
            self.ui.viz_next_button.setEnabled(False)

    def next_visualization_step(self):
        """
        Выполняет следующий шаг визуализации MD5 хеширования.
        Отображает промежуточные результаты в интерфейсе.
        """
        if not self.md5_stepper:
            return
            
        step_info, completion_msg = self.md5_stepper.next_step()
        
        if completion_msg:
            self.ui.viz_output.append(completion_msg)
            if "completed" in completion_msg.lower():
                self.ui.viz_output.append(f"\nФинальный хеш: {self.md5_stepper.get_final_hash()}")
                self.ui.viz_next_button.setEnabled(False)
                self.md5_stepper = None
        elif step_info:
            self.ui.viz_output.append(format_step_info(step_info))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MD5HasherApp()
    window.show()
    sys.exit(app.exec())
