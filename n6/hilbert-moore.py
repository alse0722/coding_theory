opt = int(input('Сжать - 0, Разжать - 1\n'))

if opt == 0:
    f = open('studies\\tkisi\\Тест_8.txt')

    d = {}
    tree = {}
    alphabet = {}
    text = ''

    while True:
        string = f.readline()
        if not string:
            break
        else:
            text += string
            for i in string:
                if i == '\n':
                    j = '*'
                elif i == ' ':
                    j = '_'
                else:
                    j = i
                if d.get(j):
                    d.update({j: d.get(j) + 1})
                else:
                    d.update({j: 1})

    f.close()

    for i in list(d.keys()):
        d.update({i: d[i]/len(text)})

    def dict_sort(d):
        sort_d = sorted(d.items(), key=lambda x: x[1])
        return dict(sort_d)

    d = dict_sort(d)

    def create_tree(d):
        keys = list(d.keys())
        r = len(keys)
        tree = {keys[0]: d[keys[0]]/2}
        for i in range(r - 1):
            tree.update({keys[i + 1]: tree[keys[i]] +
                        d[keys[i]]/2 + d[keys[i + 1]]/2})
        return tree

    def create_word(tree, j):
        start = 0.5
        ans = ''
        for i in range(j):
            if (tree > start):
                ans += '1'
                tree -= start
            else:
                ans += '0'
            start /= 2
        return ans

    def create_alphabet_help(i, tree, d):
        j = -1
        size = d[i]
        iterator = 2
        while iterator > size:
            iterator /= 2
            j += 1
        word = create_word(tree[i], j)
        return word

    def create_alphabet(tree, d):
        alphabet = {}
        for i in list(tree.keys()):
            alphabet.update({i: create_alphabet_help(i, tree, d)})
        return alphabet

    tree = create_tree(d)
    alphabet = create_alphabet(tree, d)

    f = open("res6.bin", "wb")
    keys = ''
    for i in list(alphabet.keys()):
        keys += i + ' ' + alphabet[i] + ' '
    keys += '\n'
    f.write(str(keys).encode())

    code = ''
    for i in text:
        if i == ' ':
            code += alphabet['_']
        elif i == '\n':
            code += alphabet['*']
        else:
            code += alphabet[i]

    extra_zero = 0 if len(code) % 8 == 0 else 8 - len(code) % 8
    f.write((str(extra_zero) + '\n').encode())
    bts = '0' * extra_zero + code
    to_write = bytearray()
    for i in range(0, len(bts), 8):
        to_write.append(int(bts[i: i+8], 2))

    f.write(to_write)
    f.close()

else:
    f = open("res6.bin", "rb")

    d = {}
    tree = {}
    alphabet = {}
    text = ''
    ans = ''

    str_keys = f.readline().decode()[:-2].split()
    b = True
    for i in str_keys:
        if b:
            tmp = i
            b = False
        else:
            alphabet.update({i: tmp})
            b = True

    count_of_zero = int(f.readline().decode())
    dump = f.read()
    bitstr = ''
    for b in dump:
        bits = bin(b)[2:].rjust(8, '0')
        bitstr += bits

    text = bitstr[count_of_zero:]
    f.close()

    def true_word(pos, word, text):
        if (len(word) <= len(text) - pos):
            b = True
            for i in range(len(word)):
                if word[i] == text[pos + i]:
                    b = b and True
                else:
                    b = b and False
        else:
            b = False
        return b

    i = 0
    while i < len(text):
        for j in list(alphabet.keys()):
            if true_word(i, j, text):
                ans += alphabet[j]
                i += len(j)
                break

    ans = ans.replace('_', ' ')
    ans = ans.replace('*', '\n')

    f = open("restore6.txt", "w")
    f.write(ans)
    f.close()
