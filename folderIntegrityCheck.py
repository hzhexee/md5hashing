def compare_hash_files(reference_file: str, current_file: str) -> dict:
    """
    Сравнивает два файла с хешами и возвращает результаты сравнения.

    :param reference_file: Путь к файлу с эталонными хешами.
    :param current_file: Путь к файлу с текущими хешами.
    :return: Словарь с результатами:
             - 'matched': Список файлов с совпадающими хешами.
             - 'mismatched': Список файлов с несовпадающими хешами.
             - 'missing': Список файлов, отсутствующих в текущем файле.
    """
    def parse_hash_file(file_path):
        """Читает файл с хешами и возвращает словарь {имя_файла: хеш}."""
        hash_map = {}
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]  # Пропускаем заголовок
            for line in lines:
                if ": " in line:
                    name, hash_value = line.strip().split(": ", 1)
                    hash_map[name] = hash_value
        return hash_map

    # Парсим оба файла
    reference_hashes = parse_hash_file(reference_file)
    current_hashes = parse_hash_file(current_file)

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

# Пример использования:
reference_file_path = "reference_hashes.txt"
current_file_path = "current_hashes.txt"

result = compare_hash_files(reference_file_path, current_file_path)

print("Совпадающие файлы:", result["matched"])
print("Несовпадающие файлы:", result["mismatched"])
print("Отсутствующие файлы:", result["missing"])
