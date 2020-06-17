import struct
import sys
from heapq import heappush, heappop, heapify
from collections import defaultdict

def table(txt):

    symb2freq = defaultdict(int)

    for ch in txt:
        symb2freq[ch] += 1

    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def codificar(tabla, texto):
    dict_huff = {}

    for num in tabla:
        dict_huff[num[0]] = num[1]

    txt_bin = ''

    for letra in texto:
        txt_bin += dict_huff[letra]

    return txt_bin


if __name__ == '__main__':

    archivo = sys.argv[1]

    f = open(archivo, "r")

    #Esto hay que cambiarlo por mmap
    txt = f.read()

    huff = table(txt)

    codigo_string = codificar(huff, txt)

    print(codigo_string)

    byte_list = []

    for i in range(0, len(codigo_string), 8):
        byte_list.append(codigo_string[i:(i+8)])

    print(byte_list)

    while len(byte_list[-1]) != 8: #hacemos que el ultimo byte este completo
        byte_list[-1] += '0'

    print(byte_list)

    final_list = []
    for x in byte_list:
        final_list.append(struct.pack('!B', int(x, 2)))

    print(final_list)

    # make file
    newFile = open("nuevo", "wb")
    # write to file
    for x in final_list:
        newFile.write(x)

