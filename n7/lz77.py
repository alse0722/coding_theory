import math
import struct
import time


def compression(text, file, max_buffer):
    x = 16
    max_l = int(math.pow(2, (x - math.log(max_buffer, 2))))
    buffer_pointer = 0
    l_pointer = 0
    while l_pointer < len(text):
        buffer = text[buffer_pointer:l_pointer]
        next = text[l_pointer:l_pointer + max_l]
        turple = make_turple(buffer, next)
        offset = turple[0]
        length = turple[1]
        char = bytes(turple[2], "ansi")
        shifted_offset = offset << 6
        off_length = shifted_offset + length

        byte = struct.pack(">Hc", off_length, char)
        file.write(byte)
        l_pointer += length + 1
        buffer_pointer = l_pointer - max_buffer
        if buffer_pointer < 0:
            buffer_pointer = 0


def make_turple(buffer, next):
    if len(buffer) == 0:
        return 0, 0, next[0]
    if len(next) == 0:
        return -1, -1, ""
    length = 0
    offset = 0
    tmp_buffer = buffer + next
    buffer_pointer = len(buffer)
    for i in range(len(buffer)):
        tmp_length = 0
        while tmp_buffer[i + tmp_length] == tmp_buffer[buffer_pointer + tmp_length]:
            tmp_length += 1
            if buffer_pointer + tmp_length == len(tmp_buffer):
                tmp_length -= 1
                break
            if i + tmp_length >= buffer_pointer:
                break
        if tmp_length > length:
            offset = i
            length = tmp_length
    return offset, length, tmp_buffer[buffer_pointer + length]


def decompression(input, output, max_buffer):
    i = 0
    text = ""
    while i < len(input):
        off_length, char = struct.unpack(">Hc", input[i:i+3])
        char = chr(ord(char.decode('ansi')))
        offset = off_length >> 6
        length = off_length - (offset << 6)
        i += 3
        if offset == 0 and length == 0:  # (0, 0, char)
            text += char
        else:
            pointer = len(text) - max_buffer
            if pointer < 0:
                pointer = offset
            else:
                pointer += offset
            for j in range(length):
                text += text[pointer + j]
            text += char
    output.write(text)


def main():
    print("Введите 0 для кодирования, 1 для раскодирования")
    mode = input()
    if mode == "0":
        text = (open("studies\\tkisi\\Тест_8.txt", mode='r', encoding='cp1251')).read()
        comp = open("res7.bin", mode='wb')
        start = int(round(time.time() * 1000))
        compression(text, comp, 1024)
        end = int(round(time.time() * 1000))
        print("Текст закодирован и помещен в файл Coding")
        print("Скорость кодирования: " + str((end - start)) + " мc")
    if mode == "1":
        decomp = open("restore7.txt", mode='w')
        copm_text = open("res7.bin", mode='rb').read()
        start = int(round(time.time() * 1000))
        decompression(copm_text, decomp, 1024)
        end = int(round(time.time() * 1000))
        print("Текст раскодирован и помещен в файл Decoding")
        print("Скорость декодирования: " + str((end - start)) + " мc")


if __name__ == "__main__":
    main()
