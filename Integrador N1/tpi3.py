import sys
import os

def LeerArgumentos():

    args = sys.argv
    for arg in args[0:]:
        print(arg)

def AgregarElemento(lista, elemento):
    cant = len(lista)
    i = 0
    while (i < cant and lista[i][0] != elemento): 
        i += 1

    if (i >= cant):
        lista.append([elemento, 1, ''])
    else:
        lista[i][1] += 1
        while (i > 0 and lista[i][1] > lista[i-1][1]):
            elem = lista.pop(i-1)
            lista.insert(i, elem)

            i -= 1

    return lista

def LeerArchivo(direccion):
    lista = []
    suma = 0
    with open(direccion, 'r') as arch:
        c = arch.read(1)   
        while (c):            
            lista = AgregarElemento(lista, c)
            suma += 1
            c = arch.read(1)
        arch.close()
    
    cant = len(lista)
    i = 0
    while (i < cant): 
        lista[i][1] /= suma
        i += 1
    return lista, suma

def RecorrerArbol(lista, a, b):
    
    if (b - a >= 2):            
        p = a - 1
        f = b + 1

        sump = 0.0
        sumf = 0.0

        while (f - p > 1):
            #if (sump <= sumf):
            if (sump + lista[p+1][1] <= sumf + lista[f-1][1]):
                p += 1
                lista[p][2] += '1'
                sump += lista[p][1]
            else:
                f -= 1
                lista[f][2] += '0'
                sumf += lista[f][1]

        lista = RecorrerArbol(lista, a, p)
        lista = RecorrerArbol(lista, f, b)
    else:
        if (a != b):
            lista[a][2] += '1'
            lista[b][2] += '0'
        else:
            lista[a][2] += '1'

    return lista

def Shannon_Fano(lista):
    lista = RecorrerArbol(lista, 0, len(lista) - 1)

    return lista

def BuscarIndice(lista, elemento):
    indice = 0
    cant = len(lista)    
    while (indice < cant and lista[indice][0] != elemento):
        indice += 1

    return indice

def Comprimir(direccion, lista):

    tamBits = 8

    with open('comprimido.bin', 'wb') as archC:
        cadena = ''
        with open(direccion, 'r') as arch:
            c = arch.read(1)
            while (c):
                indice = BuscarIndice(lista, c)
                cadena += lista[indice][2]

                while (len(cadena) >= tamBits - 1):
                    binario = int(cadena[0:tamBits], 2)
                    #archC.write(chr(binario))
                    archC.write(binario.to_bytes(4, byteorder='big', signed=True))
                    cadena = cadena[tamBits:]
                
                c = arch.read(1)

        if (len(cadena) > 0):
            cadena = "0" * (tamBits - len(cadena)) + cadena
            binario = int(cadena[0:tamBits], 2)
            archC.write(chr(binario))
            
        arch.close()
    archC.close()

def BuscarCodigo(lista, codigo):
    indice = 0
    cant = len(lista)    
    while (indice < cant and lista[indice][2] != codigo):
        indice += 1

    if (indice >= cant):
        indice = -1

    return indice

def Descomprimir(direccion, lista):

    tamBits = 8
    with open('descomprimido.txt', 'w') as archD:
        cadena = ''
        tam = 1
        with open('comprimido.bin', 'rb') as archC:
            c = archC.read(1)
            while (c):

                cadenaAux = bin(ord(c))[2:]
                if (len(cadenaAux) < tamBits):
                    cadenaAux = "0" * (tamBits - len(cadenaAux)) + cadenaAux
                cadena += cadenaAux
                while (tam < len(cadena)):
                    indice = BuscarCodigo(lista, cadena[0:tam])
                    if (indice != -1):
                        print(lista[indice][0])
                        archD.write(lista[indice][0])
                        cadena = cadena[tam:]
                        tam = 1
                    else:
                        tam += 1
                
                c = archC.read(1)
        archC.close()
    archD.close()

sys.setrecursionlimit(100000)
direccion = f'tp3_sample0.txt'

#LeerArgumentos()
lista, suma = LeerArchivo(direccion)
lista = Shannon_Fano(lista)

Comprimir(direccion, lista)
Descomprimir(direccion, lista)