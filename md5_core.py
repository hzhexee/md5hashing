import struct
import math

# Основные нелинейные функции
def F(x, y, z):
    """Нелинейная функция F, используемая в первом раунде MD5."""
    return (x & y) | (~x & z)

def G(x, y, z):
    """Нелинейная функция G, используемая во втором раунде MD5."""
    return (x & z) | (y & ~z)

def H(x, y, z):
    """Нелинейная функция H, используемая в третьем раунде MD5."""
    return x ^ y ^ z

def I(x, y, z):
    """Нелинейная функция I, используемая в четвертом раунде MD5."""
    return y ^ (x | ~z)

# Операция побитового циклического сдвига
def left_rotate(x, amount):
    """
    Выполняет циклический сдвиг числа влево.
    
    Args:
        x: Число для сдвига
        amount: Количество битов для сдвига
    
    Returns:
        Результат циклического сдвига
    """
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

# Инициализация констант
def md5_init():
    """
    Инициализирует начальные значения для MD5 хеширования.
    
    Returns:
        Список из четырех 32-битных констант инициализации
    """
    return [
        0x67452301,  # A
        0xEFCDAB89,  # B
        0x98BADCFE,  # C
        0x10325476   # D
    ]

# Таблица синусов
T = [int((2 ** 32) * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

# Смещения для каждого раунда
shift_amounts = [
    7, 12, 17, 22, 7, 12, 17, 22,
    7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20,
    5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23,
    4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21,
    6, 10, 15, 21, 6, 10, 15, 21
]

def md5_stream(stream):
    """
    Вычисляет MD5 хеш для входного потока данных.
    
    Args:
        stream: Файловый объект или поток байтов для хеширования
        
    Returns:
        str: MD5 хеш в виде шестнадцатеричной строки
    """
    a, b, c, d = md5_init()
    total_length = 0
    
    # Process chunks
    chunk = stream.read(64)
    while chunk:
        total_length += len(chunk)
        if len(chunk) < 64:
            break
        M = struct.unpack('<16I', chunk)
        a, b, c, d = process_chunk(a, b, c, d, M)
        chunk = stream.read(64)
    
    # Handle final chunk with padding
    chunk = bytearray(chunk)
    total_length_bits = total_length * 8
    
    # Padding
    chunk.append(0x80)
    chunk.extend([0] * (56 - len(chunk) if len(chunk) <= 56 else (120 - len(chunk))))
    chunk.extend(struct.pack('<Q', total_length_bits))
    
    # Process final chunk(s)
    for i in range(0, len(chunk), 64):
        block = chunk[i:i+64]
        if len(block) < 64:  # Pad last block if needed
            block.extend([0] * (64 - len(block)))
        M = struct.unpack('<16I', block)
        a, b, c, d = process_chunk(a, b, c, d, M)
    
    # Convert to little-endian and return result
    return '{:08x}{:08x}{:08x}{:08x}'.format(
        *[struct.unpack('<I', struct.pack('>I', x))[0] for x in (a, b, c, d)]
    )

def process_chunk(a, b, c, d, M):
    """
    Обрабатывает один 512-битный блок данных.
    
    Args:
        a, b, c, d: Текущие значения хеш-буфера
        M: 16 32-битных слов обрабатываемого блока
        
    Returns:
        tuple: Новые значения хеш-буфера
    """
    AA, BB, CC, DD = a, b, c, d
    
    for i in range(64):
        if i < 16:
            f = F(BB, CC, DD)
            g = i
        elif i < 32:
            f = G(BB, CC, DD)
            g = (5 * i + 1) % 16
        elif i < 48:
            f = H(BB, CC, DD)
            g = (3 * i + 5) % 16
        else:
            f = I(BB, CC, DD)
            g = (7 * i) % 16
        
        temp = DD
        DD = CC
        CC = BB
        BB = (BB + left_rotate((AA + f + T[i] + M[g]) & 0xFFFFFFFF, shift_amounts[i])) & 0xFFFFFFFF
        AA = temp
    
    return ((a + AA) & 0xFFFFFFFF, (b + BB) & 0xFFFFFFFF,
            (c + CC) & 0xFFFFFFFF, (d + DD) & 0xFFFFFFFF)

def md5(data):
    """
    Вычисляет MD5 хеш для входных данных.
    
    Args:
        data: Входные данные в виде bytes или bytearray
        
    Returns:
        str: MD5 хеш в виде шестнадцатеричной строки
        
    Raises:
        TypeError: Если входные данные не bytes или bytearray
    """
    if isinstance(data, (bytes, bytearray)):
        from io import BytesIO
        return md5_stream(BytesIO(data))
    raise TypeError("Data must be bytes or bytearray")

def md5_file(filepath):
    """
    Вычисляет MD5 хеш для файла.
    
    Args:
        filepath: Путь к файлу
        
    Returns:
        str: MD5 хеш файла в виде шестнадцатеричной строки
    """
    with open(filepath, "rb", buffering=65536) as f:
        return md5_stream(f)

# Хеширование строки
def md5_string(input_string):
    """
    Вычисляет MD5 хеш для строки.
    
    Args:
        input_string: Входная строка
        
    Returns:
        str: MD5 хеш строки в виде шестнадцатеричной строки
    """
    return md5(bytearray(input_string, 'utf-8'))

def integrity_check(file1_hash, file2_hash):
    """
    Проверяет целостность файлов путем сравнения их хешей.
    
    Args:
        file1_hash: MD5 хеш первого файла
        file2_hash: MD5 хеш второго файла
        
    Returns:
        bool: True если хеши совпадают, False в противном случае
    """
    return file1_hash == file2_hash

def print_step(round_num, step_num, a, b, c, d, f, g, temp):
    """
    Форматирует промежуточное состояние вычисления MD5.
    
    Args:
        round_num: Номер раунда
        step_num: Номер шага
        a, b, c, d: Текущие значения регистров
        f: Результат нелинейной функции
        g: Индекс используемого слова
        temp: Промежуточный результат
        
    Returns:
        str: Форматированная строка с информацией о текущем шаге
    """
    return (f"\nRound {round_num}, Step {step_num}:\n"
            f"A: {a:08x}  B: {b:08x}  C: {c:08x}  D: {d:08x}\n"
            f"f: {f:08x}  g: {g}\n"
            f"Temp result: {temp:08x}")

def process_chunk_with_viz(a, b, c, d, M):
    """
    Обрабатывает один 512-битный блок данных с визуализацией.
    
    Args:
        a, b, c, d: Текущие значения хеш-буфера
        M: 16 32-битных слов обрабатываемого блока
        
    Returns:
        tuple: Новые значения хеш-буфера и строка с визуализацией процесса
    """
    AA, BB, CC, DD = a, b, c, d
    output = []
    
    for i in range(64):
        if i < 16:
            f = F(BB, CC, DD)
            g = i
            round_num = 1
        elif i < 32:
            f = G(BB, CC, DD)
            g = (5 * i + 1) % 16
            round_num = 2
        elif i < 48:
            f = H(BB, CC, DD)
            g = (3 * i + 5) % 16
            round_num = 3
        else:
            f = I(BB, CC, DD)
            g = (7 * i) % 16
            round_num = 4
        
        temp = DD
        DD = CC
        CC = BB
        temp_calc = (AA + f + T[i] + M[g]) & 0xFFFFFFFF
        BB = (BB + left_rotate(temp_calc, shift_amounts[i])) & 0xFFFFFFFF
        AA = temp
        
        output.append(print_step(round_num, i % 16 + 1, AA, BB, CC, DD, f, g, temp_calc))
    
    return ((a + AA) & 0xFFFFFFFF, (b + BB) & 0xFFFFFFFF,
            (c + CC) & 0xFFFFFFFF, (d + DD) & 0xFFFFFFFF), "\n".join(output)

def md5_with_viz(data):
    """
    Вычисляет MD5 хеш с визуализацией процесса.
    
    Args:
        data: Входные данные в виде bytes или bytearray
        
    Returns:
        str: MD5 хеш в виде шестнадцатеричной строки
        
    Raises:
        TypeError: Если входные данные не bytes или bytearray
    """
    if isinstance(data, (bytes, bytearray)):
        output = []
        a, b, c, d = md5_init()
        
        data = bytearray(data)
        orig_length = len(data)
        
        data.append(0x80)
        while (len(data) % 64) != 56:
            data.append(0x00)
            
        data.extend(struct.pack('<Q', orig_length * 8))
        
        for chunk_start in range(0, len(data), 64):
            chunk = data[chunk_start:chunk_start + 64]
            M = struct.unpack('<16I', chunk)
            output.append(f"\nProcessing chunk {chunk_start//64 + 1}:")
            result, viz_output = process_chunk_with_viz(a, b, c, d, M)
            a, b, c, d = result
            output.append(viz_output)
        
        final_hash = '{:08x}{:08x}{:08x}{:08x}'.format(
            *[struct.unpack('<I', struct.pack('>I', x))[0] for x in (a, b, c, d)]
        )
        return final_hash
    raise TypeError("Data must be bytes or bytearray")

class MD5StepByStep:
    """
    Класс для пошагового вычисления MD5 хеша.
    
    Позволяет выполнять и отслеживать процесс хеширования шаг за шагом.
    """
    
    def __init__(self, data):
        """
        Инициализирует объект для пошагового вычисления MD5.
        
        Args:
            data: Входные данные в виде bytes или bytearray
            
        Raises:
            TypeError: Если входные данные не bytes или bytearray
        """
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Data must be bytes or bytearray")
        
        self.data = bytearray(data)
        self.orig_length = len(self.data)
        self.a, self.b, self.c, self.d = md5_init()
        self.current_chunk = 0
        self.current_step = 0
        self.chunks = []
        self.prepare_chunks()
        
    def prepare_chunks(self):
        """Подготавливает чанки данных для обработки, включая паддинг."""
        # Padding
        self.data.append(0x80)
        while (len(self.data) % 64) != 56:
            self.data.append(0x00)
        self.data.extend(struct.pack('<Q', self.orig_length * 8))
        
        # Split into chunks
        for i in range(0, len(self.data), 64):
            chunk = self.data[i:i+64]
            if len(chunk) < 64:
                chunk.extend([0] * (64 - len(chunk)))
            self.chunks.append(struct.unpack('<16I', chunk))

    def next_step(self):
        """
        Выполняет следующий шаг вычисления MD5.
        
        Returns:
            tuple: (информация о шаге или None, сообщение о состоянии)
        """
        if self.current_chunk >= len(self.chunks):
            return None, "Process completed"

        M = self.chunks[self.current_chunk]
        if self.current_step == 0:
            self.AA = self.a
            self.BB = self.b
            self.CC = self.c
            self.DD = self.d

        if self.current_step >= 64:
            self.a = (self.a + self.AA) & 0xFFFFFFFF
            self.b = (self.b + self.BB) & 0xFFFFFFFF
            self.c = (self.c + self.CC) & 0xFFFFFFFF
            self.d = (self.d + self.DD) & 0xFFFFFFFF
            self.current_chunk += 1
            self.current_step = 0
            return None, f"Chunk {self.current_chunk} completed"

        i = self.current_step
        if i < 16:
            f = F(self.b, self.c, self.d)
            g = i
            round_num = 1
        elif i < 32:
            f = G(self.b, self.c, self.d)
            g = (5 * i + 1) % 16
            round_num = 2
        elif i < 48:
            f = H(self.b, self.c, self.d)
            g = (3 * i + 5) % 16
            round_num = 3
        else:
            f = I(self.b, self.c, self.d)
            g = (7 * i) % 16
            round_num = 4

        temp = self.d
        self.d = self.c
        self.c = self.b
        temp_calc = (self.a + f + T[i] + M[g]) & 0xFFFFFFFF
        self.b = (self.b + left_rotate(temp_calc, shift_amounts[i])) & 0xFFFFFFFF
        self.a = temp

        self.current_step += 1
        step_info = {
            'round': round_num,
            'step': i % 16 + 1,
            'A': self.a,
            'B': self.b,
            'C': self.c,
            'D': self.d,
            'f': f,
            'g': g,
            'temp': temp_calc,
            'chunk': self.current_chunk + 1,
            'total_chunks': len(self.chunks)
        }
        
        return step_info, None

    def get_final_hash(self):
        """
        Возвращает финальный MD5 хеш.
        
        Returns:
            str: MD5 хеш в виде шестнадцатеричной строки
        """
        return '{:08x}{:08x}{:08x}{:08x}'.format(
            *[struct.unpack('<I', struct.pack('>I', x))[0] for x in (self.a, self.b, self.c, self.d)]
        )