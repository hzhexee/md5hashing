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

def md5_stream(stream):
    """Process data in chunks for memory efficiency."""
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
    """Process a single 512-bit chunk."""
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
    if isinstance(data, (bytes, bytearray)):
        from io import BytesIO
        return md5_stream(BytesIO(data))
    raise TypeError("Data must be bytes or bytearray")

def md5_file(filepath):
    with open(filepath, "rb", buffering=65536) as f:
        return md5_stream(f)

# Хеширование строки
def md5_string(input_string):
    return md5(bytearray(input_string, 'utf-8'))

def integrity_check(file1_hash, file2_hash):
    return file1_hash == file2_hash