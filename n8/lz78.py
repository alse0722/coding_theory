import struct
import time


def compression(text, file):
    tree = create_tree(text)
    for node in tree:
        pair = node[0]
        first = pair[0]
        second = bytes(pair[1], "ansi")
        byte = struct.pack(">Hc", first, second)
        file.write(byte)


def create_tree(text):
    tree = []
    not_changed = True
    first_in_pair = 0
    new_entry = True
    index = 2
    i = 1
    tree.append([[0, text[0]], 1, text[0]])
    while i < len(text):
        char = text[i]
        while new_entry:
            for j in range(len(tree)):
                if tree[j][2] == char:
                    not_changed = False
                    if i < len(text) - 1:
                        i += 1
                        char += text[i]
                        first_in_pair = j + 1
                        break
                    else:
                        char = ''
                        new_entry = False
                if j == len(tree) - 1:
                    new_entry = False
                    if not_changed:
                        char = text[i]
                        first_in_pair = 0
        pair = [first_in_pair, text[i]]
        tree.append([pair, index, char])
        index += 1
        new_entry = True
        i += 1
        not_changed = True
    return tree


def decompression(input, output):
    i = 0
    idx = 0
    tree = []
    while i < len(input):
        index, char = struct.unpack(">Hc", input[i:i+3])
        char = chr(ord(char.decode('ansi')))
        i += 3
        idx += 1
        if index == 0:
            tree.append([[index, char], idx, char])
        else:
            tree.append([[index, char], idx, (tree[index - 1][2] + char)])
    for node in tree:
        output.write(node[2])


def main():
    mode = input()  # 0 - Архивация, 1 - Разархивация
    if mode == "0":
        input_t = parse('studies\\tkisi\\Тест_3.txt')
        comp = open("res8.bin", mode='wb')
        start = int(round(time.time() * 1000))
        compression(input_t, comp)
        end = int(round(time.time() * 1000))
        print("Скорость сжатия: " + str((end - start)) + " мc")
    if mode == "1":
        decompressed = open('restore8.txt', mode='w', encoding='ansi')
        compressed = open("res8.bin", mode='rb').read()
        decompression(compressed, decompressed)


def parse(file):
    r = []
    f = open(file, "r", encoding='ansi')
    text = f.read()
    return text


if __name__ == "__main__":
    main()
