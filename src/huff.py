import sys
from heapq import heappush, heappop, heapify
from collections import defaultdict

def table(symb2freq):
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

    symb2freq = defaultdict(int)

    f = open(archivo, "r")
    txt = f.read()

    for ch in txt:
        symb2freq[ch] += 1
    # in Python 3.1+:
    # symb2freq = collections.Counter(txt)
    huff = table(symb2freq)

    codigo_string = codificar(huff, txt)

    print(codigo_string)

    #struct.pack()

