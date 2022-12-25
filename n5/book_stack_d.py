f = open("res5.bin", "rb")

alph_list = []
text = ''
ans = ''

alphabet = f.readline().decode()[:-1]
alphabet = sorted(alphabet)

count_of_zero = int(f.readline().decode())
dump = f.read()
bitstr = ''
for b in dump:
    bits = bin(b)[2:].rjust(8, '0')
    bitstr += bits

text = bitstr[count_of_zero:]
f.close()

size = 0
base = 1
while base < len(alphabet):
    base *= 2
    size += 1

pos = 0
while pos < len(text):
    tmp = ''
    for i in range(size):
        tmp += text[pos + i]
    alph_list += [tmp]
    pos += size


for i in alph_list:
    j = int(i, 2)
    ans += alphabet[j]
    tmp = alphabet.pop(j)
    alphabet = [tmp] + alphabet


ans = ans.replace('_', ' ')
ans = ans.replace('*', '\n')

f = open("restore5.txt", "w")
f.write(ans)
f.close()
