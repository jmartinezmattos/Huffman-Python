
from heapq import heappush, heappop, heapify
from collections import defaultdict

def encode(symb2freq):
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


def dehuff(code, huff):

    result = ''

    dict_dehuff = defaultdict(lambda: 2)

    for num in huff:
        dict_dehuff[num[1]] = num[0]

    temp = ''
    for digit in code:
        temp += digit
        if dict_dehuff[temp] != 2:
            result += dict_dehuff[temp]
            temp = ''



    print(result)


    # return result


if __name__ == '__main__':

    txt = "this is an example for huffman encoding hola"
    symb2freq = defaultdict(int)

    for ch in txt:
        symb2freq[ch] += 1
    # in Python 3.1+:
    # symb2freq = collections.Counter(txt)
    huff = encode(symb2freq)
    #print("Symbol\tWeight\tHuffman Code")
    #for p in huff:
    #    print ("%s\t%s\t%s" % (p[0], symb2freq[p[0]], p[1]))

    dict_huff = {}

    for num in huff:
       dict_huff[num[0]] = num[1]


    txt_bin = ''

    for letra in txt:
        txt_bin += dict_huff[letra]

    dehuff(txt_bin, huff)

    #dict_dehuff = defaultdict(lambda: 2)

    #for num in huff:
    #    dict_dehuff[num[1]] = num[0]
        #print(num)

    #print(dict_dehuff)
    #print(dict_dehuff['1000'])