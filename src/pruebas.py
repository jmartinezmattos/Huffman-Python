
if __name__ == '__main__':

    thisdict = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964
    }

    a = bin(5)

    print(a)



    new_str = ''

    size = 4

    for x in range(1, size + 1):
       new_str = new_str + a[-x]

    print(new_str)

    hola = "0123456"

    print(hola[3:])

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
            print(dict.get(buffer))
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























