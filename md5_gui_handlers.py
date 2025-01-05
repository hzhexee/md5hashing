from PyQt6.QtWidgets import QFileDialog, QApplication, QMessageBox
import os
from md5_core import md5_string, md5_file, integrity_check, md5_with_viz

def validate_hash(hash_value: str) -> bool:
    """
    Проверка, является ли строка валидным хешем.
    
    Args:
        hash_value: Строка для проверки
        
    Returns:
        bool: True если хеш валиден, False в противном случае
    """
    if not hash_value:
        return False
    if len(hash_value) != 32:
        return False
    return all(c in '0123456789abcdefABCDEF' for c in hash_value)

def show_error(parent_widget, message: str):
    """
    Вывод окна ошибки.
    
    Args:
        parent_widget: Родительский виджет
        message: Текст сообщения об ошибке
    """
    QMessageBox.critical(parent_widget, "Ошибка", message)

def compare_hash_files(reference_file: str, current_file: str) -> dict:
    """
    Сравнивает два файла с хешами и возвращает результаты сравнения.
    
    Args:
        reference_file: Путь к файлу с эталонными хешами
        current_file: Путь к файлу с текущими хешами
        
    Returns:
        dict: Словарь с результатами сравнения:
            - 'matched': Список файлов с совпадающими хешами
            - 'mismatched': Список файлов с несовпадающими хешами
            - 'missing': Список файлов, отсутствующих в текущем файле
            
    Raises:
        FileNotFoundError: Если файл не найден
        UnicodeDecodeError: При ошибке декодирования файла
        ValueError: При обнаружении некорректных хешей
    """
    try:
        def parse_hash_file(file_path):
            hash_map = {}
            # Пробуем разные кодировки для чтения файла
            encodings = ['utf-8', 'cp1251', 'windows-1251', 'ascii']
            
            for encoding in encodings:
                try:
                    with open(file_path, "r", encoding=encoding) as file:
                        lines = file.readlines()[1:]  # Пропускаем заголовок
                        for line in lines:
                            if ": " in line:
                                name, hash_value = line.strip().split(": ", 1)
                                hash_map[name] = hash_value
                    return hash_map  # Если файл успешно прочитан, возвращаем хеши
                except UnicodeDecodeError:
                    continue  # Пробуем следующую кодировку, если файл не удалось прочитать
            
            # Если не удалось прочитать файл ни с одной кодировкой, выбрасываем исключение
            raise UnicodeDecodeError(f"Could not decode file {file_path} with any of the following encodings: {encodings}")

        # Проверяем существование файлов
        if not os.path.exists(reference_file):
            raise FileNotFoundError(f"Эталонный файл не найден: {reference_file}")
        if not os.path.exists(current_file):
            raise FileNotFoundError(f"Текущий файл не найден: {current_file}")

        # Парсим оба файла
        reference_hashes = parse_hash_file(reference_file)
        current_hashes = parse_hash_file(current_file)

        # Валидация хешей
        invalid_hashes = []
        for file, hash_value in reference_hashes.items():
            if not validate_hash(hash_value):
                invalid_hashes.append(f"Некорректный хеш в эталонном файле для {file}")
        
        for file, hash_value in current_hashes.items():
            if not validate_hash(hash_value):
                invalid_hashes.append(f"Некорректный хеш в текущем файле для {file}")

        if invalid_hashes:
            raise ValueError("\n".join(invalid_hashes))

        # Сравниваем хеши
        matched = []
        mismatched = []
        missing = []

        for file, ref_hash in reference_hashes.items():
            curr_hash = current_hashes.get(file)
            if curr_hash is None:
                missing.append(file)
            elif curr_hash == ref_hash:
                matched.append(file)
            else:
                mismatched.append(file)

        return {
            "matched": matched,
            "mismatched": mismatched,
            "missing": missing
        }

    except (FileNotFoundError, UnicodeDecodeError, ValueError) as e:
        return {
            "error": str(e),
            "matched": [],
            "mismatched": [],
            "missing": []
        }

def update_hash_realtime(text, hash_output):
    """
    Обновляет хеш в реальном времени при вводе текста.
    
    Args:
        text: Введенный текст
        hash_output: Виджет для отображения хеша
    """
    try:
        if text:
            hashed_text = md5_string(text)
            if validate_hash(hashed_text):
                hash_output.setText(hashed_text)
            else:
                hash_output.setText("Ошибка хеширования")
        else:
            hash_output.clear()
    except Exception as e:
        hash_output.setText(f"Ошибка: {str(e)}")

def check_hash_string(hash_output, reference_hash_input, result_output):
    """
    Проверяет совпадение двух строковых хешей.
    
    Args:
        hash_output: Виджет с первым хешем
        reference_hash_input: Виджет со вторым хешем
        result_output: Виджет для отображения результата
    """
    hash1 = hash_output.text()
    hash2 = reference_hash_input.text()

    if not hash1 or not hash2:
        result_output.setText('Ошибка: Поля хешей не могут быть пустыми!')
        return

    if not validate_hash(hash1) or not validate_hash(hash2):
        result_output.setText('Ошибка: Некорректный формат MD5 хеша!')
        return

    if integrity_check(hash1, hash2):
        result_output.setText('Хеши совпадают!')
    else:
        result_output.setText('Хеши не совпадают!')

def on_file_button_click(parent_widget, hash_output_file):
    """
    Обрабатывает нажатие кнопки выбора файла для хеширования.
    
    Args:
        parent_widget: Родительский виджет
        hash_output_file: Виджет для отображения хеша файла
    """
    try:
        file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Выберите файл для хеширования", "", "Все файлы (*)")
        if file_path:
            if not os.path.exists(file_path):
                show_error(parent_widget, "Выбранный файл не существует!")
                return
            
            if os.path.getsize(file_path) == 0:
                show_error(parent_widget, "Файл пуст!")
                return

            hashed_text = md5_file(file_path)
            if validate_hash(hashed_text):
                hash_output_file.setText(hashed_text)
            else:
                show_error(parent_widget, "Ошибка при хешировании файла!")
        else:
            hash_output_file.clear()
    except Exception as e:
        show_error(parent_widget, f"Ошибка при обработке файла: {str(e)}")
        hash_output_file.clear()

def check_hash_file(hash_output_file, reference_hash_input_file, result_output_file):
    """
    Проверяет совпадение двух файловых хешей.
    
    Args:
        hash_output_file: Виджет с первым хешем файла
        reference_hash_input_file: Виджет со вторым хешем файла
        result_output_file: Виджет для отображения результата
    """
    hash1 = hash_output_file.text()
    hash2 = reference_hash_input_file.text()

    if not hash1 or not hash2:
        result_output_file.setText('Ошибка: Поля хешей не могут быть пустыми!')
        return

    if not validate_hash(hash1) or not validate_hash(hash2):
        result_output_file.setText('Ошибка: Некорректный формат MD5 хеша!')
        return

    if integrity_check(hash1, hash2):
        result_output_file.setText('Хеши совпадают!')
    else:
        result_output_file.setText('Хеши не совпадают!')

def on_folder_button_click(parent_widget, files_list):
    """
    Обрабатывает нажатие кнопки выбора папки для хеширования файлов.
    
    Args:
        parent_widget: Родительский виджет
        files_list: Виджет для отображения списка файлов и их хешей
    """
    folder_path = QFileDialog.getExistingDirectory(parent_widget, "Выберите папку для хеширования файлов")
    if not folder_path:
        return

    files_list.clear()
    output_file_path = os.path.join(folder_path, "file_hashes.txt")
    
    # Сначала собираем все файлы в папке
    all_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file != "file_hashes.txt":  # Пропускаем файл с хешами
                all_files.append(os.path.join(root, file))
    
    total_files = len(all_files)
    processed = 0

    with open(output_file_path, "w", buffering=65536) as output_file:
        output_file.write("Файл\tMD5 Хеш\n")
        
        for file_path in sorted(all_files):
            rel_path = os.path.relpath(file_path, folder_path)
            hashed_text = md5_file(file_path)
            
            output_line = f"{rel_path}: {hashed_text}"
            files_list.addItem(output_line)
            output_file.write(output_line + "\n")
            
            processed += 1
            if processed % 10 == 0:  # Обновляем UI после обработки каждых 10 файлов
                files_list.scrollToBottom()
                QApplication.processEvents()

    files_list.addItem(f"\nХеши файлов сохранены в {output_file_path}")

def select_reference_file(parent_widget, compare_results):
    """
    Открывает диалог выбора эталонного файла с хешами.
    
    Args:
        parent_widget: Родительский виджет
        compare_results: Виджет для отображения результатов сравнения
        
    Returns:
        str: Путь к выбранному эталонному файлу или None
    """
    file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Выберите эталонный файл с хешами", "", "Все файлы (*)")
    if file_path:
        compare_results.addItem(f"Эталонный файл выбран: {file_path}")
        return file_path
    return None

def select_current_file(parent_widget, compare_results):
    """
    Открывает диалог выбора текущего файла с хешами.
    
    Args:
        parent_widget: Родительский виджет
        compare_results: Виджет для отображения результатов сравнения
        
    Returns:
        str: Путь к выбранному текущему файлу или None
    """
    file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Выберите текущий файл с хешами", "", "Все файлы (*)")
    if file_path:
        compare_results.addItem(f"Текущий файл выбран: {file_path}")
        return file_path
    return None

def compare_files(reference_file_path, current_file_path, compare_results):
    """
    Сравнивает два файла с хешами и отображает результаты сравнения.
    
    Args:
        reference_file_path: Путь к эталонному файлу
        current_file_path: Путь к текущему файлу
        compare_results: Виджет для отображения результатов сравнения
    """
    if not reference_file_path or not current_file_path:
        compare_results.addItem("Ошибка: Не выбраны оба файла для сравнения.")
        return

    result = compare_hash_files(reference_file_path, current_file_path)

    compare_results.clear()
    if "error" in result:
        compare_results.addItem(f"Ошибка: {result['error']}")
        return

    compare_results.addItem("Совпадающие файлы:")
    compare_results.addItems(result["matched"] or ["Нет совпадений"])
    compare_results.addItem("\nНесовпадающие файлы:")
    compare_results.addItems(result["mismatched"] or ["Нет несовпадений"])
    compare_results.addItem("\nОтсутствующие файлы:")
    compare_results.addItems(result["missing"] or ["Нет отсутствующих файлов"])

def calculate_folder_hash(parent_widget, folder_hash_output):
    """
    Вычисляет хеш для всех файлов в выбранной папке.
    
    Args:
        parent_widget: Родительский виджет
        folder_hash_output: Виджет для отображения хеша папки
        
    Raises:
        Exception: При ошибке обработки папки
    """
    try:
        folder_path = QFileDialog.getExistingDirectory(parent_widget, "Выберите папку для хеширования")
        if not folder_path:
            return

        if not os.path.exists(folder_path):
            show_error(parent_widget, "Выбранная папка не существует!")
            return

        # Собираем все файлы в папке и сортируем их
        all_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                all_files.append(os.path.join(root, file))
        
        all_files.sort()
        combined_hashes = []
        
        total_files = len(all_files)
        processed = 0

        # Обрабатываеи файлы группами по 10 штук
        for file_path in all_files:
            file_hash = md5_file(file_path)
            combined_hashes.append(file_hash)
            
            processed += 1
            if processed % 10 == 0:
                folder_hash_output.setText(f"Обработано {processed}/{total_files} файлов...")
                QApplication.processEvents()
                
        # Расчет финального хеша
        final_hash = md5_string(''.join(combined_hashes))
        if validate_hash(final_hash):
            folder_hash_output.setText(final_hash)
        else:
            show_error(parent_widget, "Ошибка при вычислении хеша папки!")
    except Exception as e:
        show_error(parent_widget, f"Ошибка при обработке папки: {str(e)}")
        folder_hash_output.clear()

def check_folder_hash(current_hash, reference_hash, folder_result_output):
    """
    Проверяет совпадение хешей для папок.
    
    Args:
        current_hash: Текущий хеш папки
        reference_hash: Эталонный хеш папки
        folder_result_output: Виджет для отображения результата
    """
    if not current_hash or not reference_hash:
        folder_result_output.setText('Ошибка: Поля хешей не могут быть пустыми!')
        return

    if not validate_hash(current_hash) or not validate_hash(reference_hash):
        folder_result_output.setText('Ошибка: Некорректный формат MD5 хеша!')
        return

    if integrity_check(current_hash, reference_hash):
        folder_result_output.setText('Хеши совпадают!')
    else:
        folder_result_output.setText('Хеши не совпадают!')

def format_step_info(step_info):
    """
    Форматирование информации о шаге хеширования для вывода.
    
    Args:
        step_info: Информация о текущем шаге хеширования
        
    Returns:
        str: Отформатированная строка с информацией о шаге
    """
    if not step_info:
        return ""
    
    return (f"Чанк {step_info['chunk']}/{step_info['total_chunks']}\n"
            f"Раунд {step_info['round']}, Шаг {step_info['step']}:\n"
            f"A: {step_info['A']:08x}  B: {step_info['B']:08x}\n"
            f"C: {step_info['C']:08x}  D: {step_info['D']:08x}\n"
            f"f: {step_info['f']:08x}  g: {step_info['g']}\n"
            f"Промежуточный результат: {step_info['temp']:08x}\n")
