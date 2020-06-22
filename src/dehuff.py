#!/usr/bin/env python3

import argparse
import mmap
import sys
import struct
from os import path

MAGIC = 55555

def int_to_key(entero, size):

    a = bin(entero)

    corte = len(a) - size

    new_str = a[corte:]

    while len(new_str) < size:
        new_str = '0' + new_str

    return new_str

def crear_diccionario(tabla):

    new_dict = {}

    for x in tabla:

        key = int_to_key(x[2],x[1])

        key = key.replace('b', '0')

        new_dict[key] = x[0]

    return  new_dict

def int_to_binary_str_array(entero):
    new_str = ''

    a = bin(entero)

    for x in range(1, len(a) - 1):
        new_str = a[-x] + new_str

    while len(new_str) != 8:
        new_str = '0' + new_str

    return new_str

def create_name(name):
    i = 0
    nombre_final = ''
    while name[i] != '.':
        nombre_final += name[i]
        i += 1
    nombre_final += '.ori'
    return nombre_final

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descompresor Huffman.')
    parser.add_argument('-v', '--verbose',help='Escribe en stderr informacion sobre el avance del proceso, por ejemplo, los bitcodes para cada simbolo.',required=False, action='store_true')
    parser.add_argument('archivo', nargs='+', action='store')
    args = parser.parse_args()

    archivo = args.archivo[0]

    if not archivo.endswith('.huf'):
        raise NameError('El archivo no es .huf')

    if path.exists(create_name(archivo)):
        sys.stderr.write("El archivo '" +create_name(archivo) +" ya existe. Continuar: \n")
        answer = input()
        if answer != 's':
            sys.exit()

    f = open(archivo, "rb")

    codigo = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    #################LECTURA DE CABEZAL BEGIN ##############################

    magic_num = struct.unpack('!H', codigo[0:2])[0]

    if magic_num != MAGIC:
        raise Exception('Bad magic number')

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

    if args.verbose:
        print("Codigos huffman: \n")
        for key, value in dict.items():
            print(key, ' : ', value)

    byte = int_to_binary_str_array(codigo[inicio_encriptado])
    buffer = ''
    byte_pos = 0
    size = 0
    f = open(create_name(archivo), "w")

    while size < filelen:

        if dict.get(buffer) != None:
            f.write(dict.get(buffer))
            size += 1
            buffer = ''

        else:

            if byte_pos > 7:  # checkeamos si se termino el byte
                byte_pos = 0
                inicio_encriptado += 1
                byte = int_to_binary_str_array(codigo[inicio_encriptado])

            buffer += byte[byte_pos]
            byte_pos += 1

        if args.verbose:
            if size%10000 == 0: #cada 10000 bytes imprime cuanto va

                if size == 0:
                    porcentaje = 0
                else:
                    porcentaje = int((size/filelen)*100)

                sys.stderr.flush()
                sys.stderr.write('\rBytes impresos: ' + str(size) + ' de ' + str(filelen) + '     (' + str(porcentaje) + '%)')

    if args.verbose:
        sys.stderr.flush()
        sys.stderr.write('\rBytes impresos: ' + str(size) + ' de ' + str(filelen) + '     (100%)')

    f.close()

