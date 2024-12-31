import struct
import math

# Основные нелинейные функции
def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

# Операция побитового циклического сдвига
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

# Инициализация констант
def md5_init():
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

# Основной алгоритм MD5
def md5(data):
    if isinstance(data, (bytes, bytearray)):
        data = bytearray(data)  # Убедиться, что это bytearray
    else:
        raise TypeError("Данные должны быть байтами или bytearray")
    
    original_length = len(data) * 8  # Длина сообщения в битах
    
    # Шаг 1: Добавление битов (padding)
    data.append(0x80)
    while len(data) % 64 != 56:
        data.append(0)
    
    # Шаг 2: Добавление длины сообщения
    data += struct.pack('<Q', original_length)  # Маленький порядок байт (LE)
    
    # Шаг 3: Инициализация буфера
    a, b, c, d = md5_init()
    
    # Разбиение данных на блоки по 512 бит (64 байта)
    for chunk_offset in range(0, len(data), 64):
        chunk = data[chunk_offset:chunk_offset + 64]
        M = struct.unpack('<16I', chunk)  # Разбить блок на 16 32-битных слов
        
        # Копирование регистров
        A, B, C, D = a, b, c, d
        
        # 64 итерации цикла
        for i in range(64):
            if 0 <= i <= 15:
                f = F(B, C, D)
                g = i
            elif 16 <= i <= 31:
                f = G(B, C, D)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = H(B, C, D)
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                f = I(B, C, D)
                g = (7 * i) % 16
            
            # Основная операция
            temp = D
            D = C
            C = B
            B = (B + left_rotate(A + f + M[g] + T[i], shift_amounts[i])) & 0xFFFFFFFF
            A = temp
        
        # Обновление регистров
        a = (a + A) & 0xFFFFFFFF
        b = (b + B) & 0xFFFFFFFF
        c = (c + C) & 0xFFFFFFFF
        d = (d + D) & 0xFFFFFFFF
    
    # Результат: объединение регистров в итоговый хеш
    def to_little_endian(n):
        return struct.unpack('<I', struct.pack('>I', n))[0]
    
    a = to_little_endian(a)
    b = to_little_endian(b)
    c = to_little_endian(c)
    d = to_little_endian(d)
    
    return '{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d)

# Хеширование строки
def md5_string(input_string):
    return md5(bytearray(input_string, 'utf-8'))

# Хеширование файла
def md5_file(filepath):
    with open(filepath, "rb") as f:
        file_data = f.read()  # Чтение файла полностью
    return md5(file_data)

def integrity_check(file1_hash, file2_hash):
    return file1_hash == file2_hash