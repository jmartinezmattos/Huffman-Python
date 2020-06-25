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


def calc_force(huff, frecuencia):
    '''Calculates the size of the resulting compressed file without header using codes table (huff) and frequenci table (frecuencia)'''
    size = 0

    for x in huff:
        size += frecuencia[x[0]]*len(x[1])

    size = size/8 ##paso de bits a bytes

    return size

def table(txt, verbose = False):
    ''''Creates table of huffman codes of each character in txt. Use verbose = True if you want to print information during process'''
    symb2freq = defaultdict(int)

    if verbose:
        sys.stderr.write('Contando frecuencia de caracteres...\n')

    for ch in txt:
        symb2freq[ch] += 1#importante

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

    huff = sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

    size = calc_force(huff, symb2freq)

    return [huff, size]

def obtener_dict(tabla):
    '''Creates a dictionary using tabla'''
    huff_dict = {}

    for num in tabla:
        huff_dict[num[0]] = num[1]

    return huff_dict

def create_name(name):
    '''Replaces the extension of name with .huf'''
    i = 0
    nombre_final = ''
    while name[i] != '.':
        nombre_final += name[i]
        i += 1
    nombre_final += '.huf'
    return nombre_final


def crear_cabezal(archivo, sym_arraylen, sym_arraysize, magic):
    '''Creates header'''
    magic_nbr = struct.pack('!H', magic)#dos bytes
    sym_arraylen = struct.pack('B',sym_arraylen)#un byte
    sym_arraysize = struct.pack('!B', sym_arraysize) #no se si esto esta bien le puse 8 por la cantidad de bits
    filelen = struct.pack('!I', os.path.getsize(archivo))#cuatro bytes

    cabezal = [magic_nbr, sym_arraylen, sym_arraysize, filelen]

    return cabezal

def elements_array(huff):
    '''Creates part of header containing huffman codes'''
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
    '''Esto no es necesario, solo es una animacion re piola'''
    for c in itertools.cycle(['|', '/', '-', '\\']):
       if done:
            break
       sys.stderr.write(f'\rProcesando... {c} ')
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

    archivo = args.archivo[0]

    f = open(archivo, "r")

    txt = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    huff, compress_size = table(txt, args.verbose)

    compress_size = int(compress_size + len(huff)*6 + 8)##Este int es para redondear porque compress_size es float

    if args.verbose:
        sys.stderr.write(f'Original size: {os.path.getsize(archivo)} bytes\n' )
        sys.stderr.write(f"Compress size: {compress_size} bytes \n")
        ##Esto de abajo es solo para una animacion (ver funcion animate)
        ##t = threading.Thread(target=animate)
        ##t.start()


    huff_dict = obtener_dict(huff)

    if args.verbose:
        sys.stderr.write('\nTabla huffman completada:\n\n')

        for x in huff:
            sys.stderr.write(str(x[0]) + ' = ' + str(x[1]) + '\n') ## x[0] es el caracter y x[1] el codigo huff

    if args.verbose:
        sys.stderr.write('\nCodificando texto...\n')

    newFile = open(create_name(archivo), "wb")

    elementos = elements_array(huff)

    cabezal = crear_cabezal(archivo, len(elementos), 6, 55555)

    if args.force:
        print("Compresion forzada")
    else:
        if compress_size > os.path.getsize(archivo): ##Hay que agregarle size del header a esto
            raise Exception("El archivo comprimido es mas grande")

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

    buffer_write = ''
    buffer_store = ''

    for letra in txt:
        obtener = huff_dict[letra] ##obtengo el codigo huff de la letra

        buffer_store += obtener

        while len(buffer_write) != 8 and len(buffer_store) != 0:
            buffer_write += buffer_store[0]
            if len(buffer_store) == 1:
                buffer_store = ''
            else:
                buffer_store = buffer_store[1:]

        if len(buffer_write) == 8:
           binario = struct.pack('!B', int(buffer_write, 2))
           newFile.write(binario)
           buffer_write = ''

    while len(buffer_store) != 0:

        while len(buffer_write) < 8:
            if len(buffer_store) !=0:
                buffer_write += buffer_store[0]
                if len(buffer_store) == 1:
                    buffer_store = ''
                else:
                    buffer_store = buffer_store[1:]
            else:
                buffer_write += '0'

        binario = struct.pack('!B', int(buffer_write, 2))
        newFile.write(binario)
        buffer_write = ''

    done = True
