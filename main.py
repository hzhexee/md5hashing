import sys
from PyQt6.QtWidgets import QApplication, QWidget
from md5_hasher_ui import Ui_MD5HasherApp
from md5_gui_handlers import *

class MD5HasherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the UI from the generated class
        self.ui = Ui_MD5HasherApp()
        self.ui.setupUi(self)

        # Load and apply stylesheet
        with open('md5_gui_styles.css', 'r') as file:
            self.setStyleSheet(file.read())

        # Store file paths for comparison
        self.reference_file_path = None
        self.current_file_path = None

        # Connect signals to slots
        self.setup_connections()

    def setup_connections(self):
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

    # Handler methods that connect to the existing handler functions
    def update_hash_realtime(self, text):
        update_hash_realtime(text, self.ui.hash_output)

    def check_hash_string(self):
        check_hash_string(self.ui.hash_output, self.ui.reference_hash_input, self.ui.result_output)

    def on_file_button_click(self):
        on_file_button_click(self, self.ui.hash_output_file)

    def check_hash_file(self):
        check_hash_file(self.ui.hash_output_file, self.ui.reference_hash_input_file, self.ui.result_output_file)

    def on_folder_button_click(self):
        on_folder_button_click(self, self.ui.files_list)

    def select_reference_file(self):
        self.reference_file_path = select_reference_file(self, self.ui.compare_results)

    def select_current_file(self):
        self.current_file_path = select_current_file(self, self.ui.compare_results)

    def compare_files(self):
        compare_files(self.reference_file_path, self.current_file_path, self.ui.compare_results)

    def calculate_folder_hash(self):
        calculate_folder_hash(self, self.ui.folder_hash_output)

    def check_folder_hash(self):
        check_folder_hash(
            self.ui.folder_hash_output.text(),
            self.ui.folder_reference_hash_input.text(),
            self.ui.folder_result_output
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MD5HasherApp()
    window.show()
    sys.exit(app.exec())
