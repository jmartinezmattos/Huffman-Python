#!/usr/bin/env python3

import argparse
import mmap
import os
import struct
import sys
from heapq import heappush, heappop, heapify
from collections import defaultdict

import itertools
import threading
import time


def table(txt, verbose = False):

    symb2freq = defaultdict(int)

    if verbose:
        sys.stderr.write('Contando frecuencia de caracteres...\n')

    for ch in txt:
        symb2freq[ch] += 1

    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)

    if verbose:
        sys.stderr.write('Calculando codigos huffman...\n')

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

def create_name(name):
    i = 0
    nombre_final = ''
    while name[i] != '.':
        nombre_final += name[i]
        i += 1
    nombre_final += '.huf'
    return nombre_final

def to_binary(entrada, bits=8, pack_format = 'B'):

    byte_list = []
    for i in range(0, len(entrada), bits):  # separo en bytes
        byte_list.append(entrada[i:(i + bits)])

    while len(byte_list[-1]) != bits:  # hacemos que el ultimo byte este completo
        byte_list[-1] += '0'

    final_list = []
    pack_form = '!' + pack_format
    for x in byte_list:
        final_list.append(struct.pack(pack_form, int(x, 2)))

    return final_list

def crear_cabezal(archivo, sym_arraylen, sym_arraysize, magic):

    magic_nbr = struct.pack('!H', magic)#dos bytes
    sym_arraylen = struct.pack('B',sym_arraylen)#un byte
    sym_arraysize = struct.pack('!B', sym_arraysize) #no se si esto esta bien le puse 8 por la cantidad de bits
    filelen = struct.pack('!I', os.path.getsize(archivo))#cuatro bytes

    cabezal = [magic_nbr, sym_arraylen, sym_arraysize, filelen]

    return cabezal

def elements_array(huff):

    lista_total = []

    for x in huff:
        lista_individual = []
        #Primer byte es el simbolo
        lista_individual.append(struct.pack('!B', ord(x[0])))
        #Segundo byte es valor entero que indica cantidad de bits que usa el codigo huffman
        lista_individual.append(struct.pack('!B', len(x[1])))
        #bytes del 3 al 6 son el codigo huffman
        lista_individual.append(struct.pack('!I', int(x[1], 2)))

        #agregamos a la lista total
        lista_total.append(lista_individual)

    return lista_total

def animate():
       for c in itertools.cycle(['|', '/', '-', '\\']):
           if done:
               break
           sys.stderr.write('\rProcesando... ' + c +' ')
           sys.stderr.flush()
           time.sleep(0.1)
       sys.stdout.write('\rProceso terminado!     ')

if __name__ == '__main__':

    done = False

    parser = argparse.ArgumentParser(description='Compresor Huffman')
    parser.add_argument('-f', '--force', help='forzar la compresion, aunque el archivo resultante sea mas grande', required=False, action='store_true')
    parser.add_argument('-v', '--verbose', help='escribe en stderr informacion sobre el avance del proceso,por ejemplo, los bitcodes para cada simbolo', required=False, action='store_true')
    parser.add_argument('archivo', nargs='+', action='store')
    args = parser.parse_args()

    t = threading.Thread(target=animate)
    t.start()

    if args.force:
        print("Forzado")

    archivo = args.archivo[0]

    f = open(archivo, "r")

    txt = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    huff = table(txt, args.verbose)

    if args.verbose:
        sys.stderr.write('\nTabla huffman completada:\n\n')

        for x in huff:
            sys.stderr.write(str(x[0]) + ' = ' + str(x[1]) + '\n')

    if args.verbose:
        sys.stderr.write('\nCodificando texto...\n')

    codigo_string = codificar(huff, txt)

    final_list = to_binary(codigo_string)

    elementos = elements_array(huff)

    cabezal = crear_cabezal(archivo, len(elementos), 6, 55555)

    newFile = open(create_name(archivo), "wb")

    if args.verbose:
        sys.stderr.write('Escribiendo cabezal...\n')
    for x in cabezal:
        newFile.write(x)

    if args.verbose:
        sys.stderr.write('Escribiendo elementos...\n')
    for x in elementos:
        for y in x:
            newFile.write(y)

    if args.verbose:
        sys.stderr.write('Escribiendo texto codificado...\n')
    for x in final_list:
        newFile.write(x)

    done = True
