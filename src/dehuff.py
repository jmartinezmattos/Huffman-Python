import argparse
import mmap
from collections import defaultdict
import struct

#f = open('comprimido.hof', 'rb') #en modo read binary

#for x in f:
#    #lee cada byte
#    pass

def int_to_key(entero, size):

    a = bin(entero)

    corte = len(a) - size

    new_str = a[corte:]

    return new_str

def crear_diccionario(tabla):

    new_dict = {}

    for x in tabla:

        key = int_to_key(x[2],x[1])

        key = key.replace('b', '0')

        new_dict[key] = x[0]

    return  new_dict

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

def int_to_binary_str_array(entero):
    new_str = ''

    a = bin(entero)

    for x in range(1, len(a) - 1):
        new_str = a[-x] + new_str

    while len(new_str) != 8:
        new_str = '0' + new_str

    return new_str

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Huffman')
    parser.add_argument('-v', '--verbose',help='escribe en stderr información sobre el avance del proceso,por ejemplo, los bitcodes para cada símbolo',required=False, action='store_true')
    parser.add_argument('archivo', nargs='+', action='store')
    args = parser.parse_args()

    archivo = args.archivo[0]  ##no se por que es asi pero funciona

    f = open(archivo, "rb")

    codigo = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    #################LECTURA DE CABEZAL BEGIN ##############################

    magic_num = struct.unpack('!H', codigo[0:2])[0]

    sym_arraylen = codigo[2]

    sym_arraysize = codigo[3]

    filelen = struct.unpack('!I', codigo[4:8])[0]

    #################LECTURA DE CABEZAL END ##############################



    #################LECTURA ELEMENTOS BEGIN ##############################

    largo_elementos = sym_arraysize * sym_arraylen

    inicial = 8

    elementos = []

    for x in range(0, largo_elementos, sym_arraysize):
        codigo_simbolo = []

        simbolo = chr(codigo[inicial + x])

        largo_huff = codigo[inicial + x + 1]

        codigo_huff = struct.unpack('!I', codigo[inicial + x + 2: inicial + x + 6])[0]

        codigo_simbolo = [simbolo, largo_huff, codigo_huff]

        elementos.append(codigo_simbolo)

    #################LECTURA ELEMENTOS END ##############################

    inicio_encriptado = largo_elementos + inicial

    dict = crear_diccionario(elementos)

    byte = int_to_binary_str_array(codigo[inicio_encriptado])
    buffer = ''
    byte_pos = 0
    encontrado = False
    size = 0
    f = open("Salida.txt", "w")

    while size < filelen:

        if dict.get(buffer) != None:
            f.write(dict.get(buffer))
            size += 1
            encontrado = True

        if encontrado:
            buffer = ''
            encontrado = False

        else:

            if byte_pos > 7:  # checkeamos si se termino el byte
                byte_pos = 0
                inicio_encriptado += 1
                byte = int_to_binary_str_array(codigo[inicio_encriptado])

            buffer += byte[byte_pos]
            byte_pos += 1

    f.close()

