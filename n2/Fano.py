import time

ans = int(input('Сжать - 0, Разжать - 1\n'))

if ans == 0:

    a = open('studies\\tkisi\\Тест_8.txt')
    start_time = time.perf_counter()
    text = a.read()
    input_text = text
    d = []
    alph = []
    # Пробежимся по строке и будем добавлять в список пары (частота, символ) а затем удалять все вхождения символа из строки
    l_t = len(text)
    while len(text) > 0:
        x = text[0]
        alph.append(x)
        d.append((text.count(x)/l_t, x))
        text = text.replace(x, '')

    # Сортировка списка будет моделировать очередь с приоритетом
    d.sort()
    d = d[::-1]
    # Создадим дерево таким образом:
    #   Будем добавлять в дерево вершины в виде - имя_вершины : (имя_родителя, метка пути к родителю)
    d_1 = {}
    node_1 = ''
    for x in d:
        d_1[x[1]] = x[0]
        node_1 += x[1]

    tree = {}

    tree[node_1] = (1, -1, -1)
    q = [node_1]

    while len(q) > 0:
        parent = q[0]
        if len(parent) == 1:
            q = q[1:]
            continue
        c1 = ''
        c2 = ''
        c1p = 0
        c2p = 0
        for x in parent:
            if c1p < 0.5:
                c1p += d_1[x] / tree[parent][0]
                d_1[x] = d_1[x] / tree[parent][0]
                c1 += x
            else:
                c2p += d_1[x] / tree[parent][0]
                d_1[x] = d_1[x] / tree[parent][0]
                c2 += x
        tree[c1] = (c1p, 0, parent)
        if c2 != '':
            tree[c2] = (c2p, 1, parent)
        q = q[1:]
        q.append(c1)
        if c2 != '':
            q.append(c2)

    #if len(d) == 1: tree[d[0][1]] =  (d[0][1]+d[0][1], 1)
    print(tree)

    dictionary = {}
    l = list(tree.keys())
    for x in alph:
        s = ''
        z = x
        while True:
            if tree[z][2] != -1:
                s = str(tree[z][1]) + s
                z = tree[z][2]
            else:
                break
        reversed(s)
        dictionary[x] = s

    print('Сопоставим исходным символам их код: ', dictionary)

    bin_file = open('res2.bin', 'wb+')
    l = list(dictionary.keys())
    bin_file.write(b' ')
    for x in l:
        s2 = int(dictionary[x], 2)
        bin_file.write(x.encode())
        bin_file.write(dictionary[x].encode())
        bin_file.write(b' ')

    if (l.count('\n') == 0):
        bin_file.write(b'\n')
    s = ''
    bin_file.write(b'\n')
    for x in input_text:
        s += dictionary[x]
    #print('\n', s, len(s))

    if len(s) % 8 != 0:
        bin_file.write(str((8*(len(s)//8) + 8 - len(s))).encode())
        s = '0' * (8*(len(s)//8) + 8 - len(s)) + s
    else:
        bin_file.write((str(0)).encode())
    bin_file.write(b'\n')

    #print('\n', s, len(s))

    while s != '':
        sub = s[0:8]
        s = s[8:]
        s1 = int(sub, 2)
        s2 = s1.to_bytes((s1.bit_length() + 7) // 8, 'big')
        bin_file.write(s1.to_bytes((s1.bit_length() + 7) // 8, 'big'))
    bin_file.close()

    print("--- %s seconds ---" % (time.perf_counter() - start_time))


else:

    bf = open('res2.bin', 'rb')

    start_time = time.perf_counter()

    decode_text = bf.readline().decode('utf-8')
    decode_text += bf.readline().decode('utf-8')
    decode_text += bf.readline().decode('utf-8')
    # print(decode_text)

    output_text = bf.read()
    a = ''
    for x in output_text:
        a += '0' * (8 - len(bin(x)[2:])) + bin(x)[2:]

    if len(a) % 8 != 0:
        a = '0' * (8*(len(a)//8) + 8 - len(a)) + a

    output_text = decode_text + a

    # print(output_text)

    dec_dict = {}

    t = 0
    a = ''
    t2 = 0
    for x in output_text:
        if x == '\n' and t == 1:
            break
        if x == '\n':
            t += 1
        if x != ' ':
            a += x
            if t2 != 0:
                t2 = 0
        if x == ' ' and t2 == 1:
            t2 = -1
            a += x
        if x == ' ' and t2 != -1 and a != '':
            t2 = 1
            dec_dict[a[1:]] = a[0]
            a = ''

    output_text = output_text[output_text.index('\n')+1:]
    output_text = output_text[output_text.index('\n')+1:]

    zero = int(output_text[0])
    output_text = output_text[zero+2:]
    #print(dec_dict, output_text)

    out_f = open('restore2.txt', 'w')

    final_text = ''
    a = ''
    l = list(dec_dict.keys())
    for x in output_text:
        a += x
        if l.count(a) != 0:
            out_f.write(dec_dict[a])
            #final_text += dec_dict[a]
            a = ''

    print("--- %s seconds ---" % (time.perf_counter() - start_time))
