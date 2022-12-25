import sys
import getopt
sys.path.insert(0, "studies\\tkisi")
from tree import Node
import array
import time

class FGK(object):
    def __init__(self):
        super(FGK, self).__init__()
        self.NYT = Node(symbol="NYT")
        self.root = self.NYT
        self.nodes = []
        self.seen = [None] * 10000

    def get_code(self, s, node, code=''):
        if node.left is None and node.right is None:
            return code if node.symbol == s else ''
        else:
            temp = ''
            if node.left is not None:
                temp = self.get_code(s, node.left, code+'0')
            if not temp and node.right is not None:
                temp = self.get_code(s, node.right, code+'1')
            return temp

    def find_largest_node(self, weight): # просто пробегаемся по списку вершин в обратном порядке 
        for n in reversed(self.nodes): # и выбираем вершину с весом равным заданному 
            if n.weight == weight:
                return n

    def swap_node(self, n1, n2):
        i1, i2 = self.nodes.index(n1), self.nodes.index(n2) # В общем списке всех элементов найдем номера данных двух
        self.nodes[i1], self.nodes[i2] = self.nodes[i2], self.nodes[i1] # и в списке поменяем их местами

        tmp_parent = n1.parent # поменяем им их родителей
        n1.parent = n2.parent
        n2.parent = tmp_parent

        if n1.parent.left is n2: # если второй был левым потомком своего родителя
            n1.parent.left = n1 # то первй станет левым
        else:
            n1.parent.right = n1 # иначе правым

        if n2.parent.left is n1: # аналогично
            n2.parent.left = n2
        else:
            n2.parent.right = n2

    def insert(self, s): #Добавление символа в дерево
        node = self.seen[ord(s)] #Проверим присутствует ли наш элемент в списке из всевозможных 256 элементов 

        if node is None:  # Если нет, то мы встретили его впервые
            spawn = Node(symbol=s, weight=1)  # создадим новый лист в дереве
            internal = Node(symbol='', weight=1, parent=self.NYT.parent,  # на месте старого NYT создадим вершину с весом 1 и пустым именем
                left=self.NYT, right=spawn) #  родителем которой станет бывший родитель NYT
            spawn.parent = internal # Эта вершина станет родителем для нового листа
            self.NYT.parent = internal # И для нового NYT

            if internal.parent is not None:  # Если у нового узла не пустой родитель 
                internal.parent.left = internal # то скажем что левым потомком этого родителя становится наш новый узел
            else:
                self.root = internal # иначе этот узел корень

            self.nodes.insert(0, internal) # В список вершин строящегося дерева добавим новый узел
            self.nodes.insert(0, spawn) # и новый лист

            self.seen[ord(s)] = spawn # В списке всевозможных элементов отметим новый лист как уже встретившийся
            node = internal.parent 

        # Обновим дерево
        while node is not None: # пока не дошли до пустой вершины (несуществующий отец корня дерева)
            largest = self.find_largest_node(node.weight)

            if (node is not largest and node is not largest.parent and
                largest is not node.parent): # если текущая вершина сама не наибольшая и не ее родитель и не ее потомок 
                self.swap_node(node, largest) # то поменяем их местами

            node.weight = node.weight + 1
            node = node.parent

    def encode(self, text):
        result = ''

        for s in text:
            if self.seen[ord(s)]: # if symbol already seen then return code
                result += self.get_code(s, self.root)
            else:
                result += self.get_code('NYT', self.root)  # else code of NYT followed by the code of the symbol
                result += bin(ord(s))[2:].zfill(8)

            self.insert(s)

        return result

    def get_symbol_by_ascii(self, bin_str):
        return chr(int(bin_str, 2))

    def decode(self, text):
        result = ''

        symbol = self.get_symbol_by_ascii(text[:8])
        result += symbol
        self.insert(symbol)
        node = self.root

        i = 8
        while i < len(text):  # читаем побитово
            node = node.left if text[i] == '0' else node.right # Переходим в левого потомка если 0, если 1 то в правого
            symbol = node.symbol

            if symbol:  # если это не лист и не корень то есть имя этой вершины не пустое
                if symbol == 'NYT': # и если случилось так что мы этим путем из 0 и 1 дошли до NYT 
                    symbol = self.get_symbol_by_ascii(text[i+1:i+9]) # то дальше будет символ и его нужно считать
                    i += 8 # его длинна была 8 бит и его нужно перешагнуть

                result += symbol
                self.insert(symbol)
                node = self.root

            i += 1

        return result

def bytes2bits (textbin):
    byte = textbin.read(1)
    bincode = ""
    lastcode = ""
    while byte:
        code = str(int(bin(int.from_bytes(byte, byteorder="little"))[2:]))
        lastcode = code
        if len(code) < 8:
            code = "0" * (8 - len(code)) + code
        bincode += code
        byte = textbin.read(1)
    bincode = bincode[:-7]
    bincode += lastcode
    return bincode



def main(argv = '-e studies\\tkisi'):
    argv = []
    e_d = 'd'
    body = 'Compressed'
    r = 'bin'
    for i in range(11, 12):
        argv.append( f'-{e_d}  studies\\tkisi\\{body}{i}.{r}'.split('  ')[0] )
        argv.append( f'-{e_d}  studies\\tkisi\\{body}{i}.{r}'.split('  ')[1] )
           
    try:
        opts, args = getopt.getopt(argv, "e:d:")
    except getopt.GetoptError:
        sys.exit(2)

    text = None
    result = None
    i = 11
    for opt, arg in opts:
        if opt == '-e':
            with open(arg) as f:
                text = f.read()
            datac = array.array('B')
            start = int(round(time.time() * 1000))
            result = str(FGK().encode(text))
            copm_text = (open(f"Compressed{i}.txt", mode='w'))
            bintext = (open(f"Compressed{i}.bin", mode="wb"))
            tmp = result
            while len(result) > 0:
                datac.append(int(result[:8], 2))
                result = result[8:]
            end = int(round(time.time() * 1000))
            datac.tofile(bintext)
            end = int(round(time.time() * 1000))
            print ("The speed is: " + str((end - start)) + " ms")
            copm_text.write(tmp)
            copm_text.close()
            bintext.close()
            i += 1
        elif opt == '-d':
            with open(arg, 'rb') as f:
                bincode = bytes2bits(f)
            result = FGK().decode(bincode)
            decomp = open(f"Original{i}.txt", mode='w')
            decomp.write(result)
            decomp.close()


if __name__ == '__main__':
    main(sys.argv[1:])