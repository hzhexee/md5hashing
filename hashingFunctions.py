from PyQt6.QtWidgets import QFileDialog
import os
from md5_hashing import md5_string, md5_file, integrity_check
from folderIntegrityCheck import compare_hash_files

def update_hash_realtime(text, hash_output):
    if text:
        hashed_text = md5_string(text)
        hash_output.setText(hashed_text)
    else:
        hash_output.clear()

def check_hash_string(hash_output, reference_hash_input, result_output):
    hash1 = hash_output.text()
    hash2 = reference_hash_input.text()

    if integrity_check(hash1, hash2):
        result_output.setText('Хеши совпадают!')
    else:
        result_output.setText('Хеши не совпадают!')

def on_file_button_click(parent_widget, hash_output_file):
    file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Выберите файл для хеширования", "", "Все файлы (*)")
    if file_path:
        hashed_text = md5_file(file_path)
        hash_output_file.setText(hashed_text)
    else:
        hash_output_file.clear()

def check_hash_file(hash_output_file, reference_hash_input_file, result_output_file):
    hash1 = hash_output_file.text()
    hash2 = reference_hash_input_file.text()

    if integrity_check(hash1, hash2):
        result_output_file.setText('Хеши совпадают!')
    else:
        result_output_file.setText('Хеши не совпадают!')

def on_folder_button_click(parent_widget, files_list):
    folder_path = QFileDialog.getExistingDirectory(parent_widget, "Выберите папку для хеширования файлов")
    if folder_path:
        files_list.clear()

        output_file_path = os.path.join(folder_path, "file_hashes.txt")

        with open(output_file_path, "w") as output_file:
            output_file.write("Файл\tMD5 Хеш\n")

            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    hashed_text = md5_file(file_path)

                    files_list.addItem(f"{file}: {hashed_text}")
                    output_file.write(f"{file}: {hashed_text}\n")

        files_list.addItem(f"\nХеши файлов сохранены в {output_file_path}")

def select_reference_file(parent_widget, compare_results):
    file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Выберите эталонный файл с хешами", "", "Все файлы (*)")
    if file_path:
        compare_results.addItem(f"Эталонный файл выбран: {file_path}")
        return file_path
    return None

def select_current_file(parent_widget, compare_results):
    file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Выберите текущий файл с хешами", "", "Все файлы (*)")
    if file_path:
        compare_results.addItem(f"Текущий файл выбран: {file_path}")
        return file_path
    return None

def compare_files(reference_file_path, current_file_path, compare_results):
    if not reference_file_path or not current_file_path:
        compare_results.addItem("Ошибка: Не выбраны оба файла для сравнения.")
        return

    result = compare_hash_files(reference_file_path, current_file_path)

    compare_results.clear()
    compare_results.addItem("Совпадающие файлы:")
    compare_results.addItems(result["matched"] or ["Нет совпадений"])
    compare_results.addItem("\nНесовпадающие файлы:")
    compare_results.addItems(result["mismatched"] or ["Нет несовпадений"])
    compare_results.addItem("\nОтсутствующие файлы:")
    compare_results.addItems(result["missing"] or ["Нет отсутствующих файлов"])

def calculate_folder_hash(parent_widget, folder_hash_output):
    folder_path = QFileDialog.getExistingDirectory(parent_widget, "Выберите папку для хеширования")
    if folder_path:
        combined_hashes = ""
        
        all_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        
        all_files.sort()

        for file_path in all_files:
            file_hash = md5_file(file_path)
            combined_hashes += file_hash

        final_hash = md5_string(combined_hashes)
        folder_hash_output.setText(final_hash)

def check_folder_hash(current_hash, reference_hash, folder_result_output):
    if not current_hash or not reference_hash:
        folder_result_output.setText('Ошибка: Отсутствует текущий или эталонный хеш')
        return

    if integrity_check(current_hash, reference_hash):
        folder_result_output.setText('Хеши совпадают!')
    else:
        folder_result_output.setText('Хеши не совпадают!')
