import argparse
import mmap
from collections import defaultdict
import struct

#f = open('comprimido.hof', 'rb') #en modo read binary

#for x in f:
#    #lee cada byte
#    pass

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
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Huffman')
    parser.add_argument('-v', '--verbose',help='escribe en stderr información sobre el avance del proceso,por ejemplo, los bitcodes para cada símbolo',required=False, action='store_true')
    parser.add_argument('archivo', nargs='+', action='store')
    args = parser.parse_args()

    archivo = args.archivo[0]  ##no se por que es asi pero funciona

    f = open(archivo, "rb")

    codigo = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    magic_num = [codigo[0], codigo[1]]

    print(magic_num)
