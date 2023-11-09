import sys
import os
import math

BITE_SIZE = 8

def LeerArgumentos():
    args = sys.argv
    for arg in args[0:]:
        print(arg)

#Metodos Binarios
def IntToBinary(num):
    return num.to_bytes(1, byteorder='big')
def ChrToBinary(character):
    return character.encode('utf-8')
def StringToBinary(cadena, right = False):
    if (right):        
        cadena = cadena + "0" * (BITE_SIZE - len(cadena))   
    numero_entero = int(cadena, 2)
    bytes_binarios = numero_entero.to_bytes(1, byteorder='big')

    return bytes_binarios

def BinaryToChr(byte):
    return chr(int.from_bytes(byte, byteorder='big'))
def BinaryToInt(byte):
    return int.from_bytes(byte, byteorder='big')
def BinaryToString(byte):
    cadenaAux = bin(ord(byte))[2:]
    if (len(cadenaAux) < BITE_SIZE):
        cadenaAux = "0" * (BITE_SIZE - len(cadenaAux)) + cadenaAux
    return cadenaAux
#Metodos Generales
def AgregarElemento(lista, elemento):
    cant = len(lista)
    i = 0
    while (i < cant and lista[i][0] != elemento): 
        i += 1

    if (i >= cant):
        lista.append([elemento, 1, ''])
    else:
        lista[i][1] += 1
        if (i > 0):
            valor = lista[i][1]
            indice = i
            i -= 1
            while (i > 0 and valor > lista[i][1]):
                i -= 1                
            lista.insert(i, lista.pop(indice))            

    return lista
def BuscarIndice(lista, elemento):
    indice = 0
    cant = len(lista)    
    while (indice < cant and lista[indice][0] != elemento):
        indice += 1

    return indice
def BuscarCodigo(lista, codigo):
    indice = 0
    cant = len(lista)    
    while (indice < cant and lista[indice][1] != codigo):
        indice += 1

    if (indice >= cant):
        indice = -1

    return indice

#Comprimir
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
    return lista

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

def GuardarTabla(arch, lista):
    arch.write(IntToBinary(len(lista)))

    for l in lista:
        arch.write(ChrToBinary(l[0]))
        tam = len(l[2])
        arch.write(IntToBinary(tam))
            
        codigo = l[2]
        while (tam > BITE_SIZE):
            cadena = StringToBinary(codigo[:BITE_SIZE])
            arch.write(cadena)
            codigo = codigo[BITE_SIZE:]
            tam = len(codigo)

        if (tam < BITE_SIZE):
            codigo = StringToBinary(codigo, True)
        else:
            codigo = StringToBinary(codigo)
        arch.write(codigo)

def Comprimir(original, compression):
        
    lista = LeerArchivo(original)
    lista = Shannon_Fano(lista)

    with open(compression, 'wb') as archC:
        GuardarTabla(archC, lista)
        cadena = ''
        print(lista)
        with open(original, 'r') as arch:
            c = arch.read(1)
            while (c):
                indice = BuscarIndice(lista, c)
                cadena += lista[indice][2]

                while (len(cadena) > BITE_SIZE):
                    archC.write(StringToBinary(cadena[:BITE_SIZE]))
                    cadena = cadena[BITE_SIZE:]
                
                c = arch.read(1)

        if (len(cadena) > 0):
            archC.write(StringToBinary(cadena, right=True))
            
        arch.close()
    archC.close()

#Descomprimir
def CargarTabla(arch):
    lista = []

    byte = arch.read(1)
    tam = BinaryToInt(byte)
    j = 0
    while (byte and j < tam):
        byte = arch.read(1)
        caracter = BinaryToChr(byte)

        byte = arch.read(1)
        long = BinaryToInt(byte)
        cant = math.ceil(long / BITE_SIZE)
        codigo = ''
        for i in range(cant):
            byte = arch.read(1)
            codigo = codigo + BinaryToString(byte)
        codigo = codigo[0:long]

        lista.append([caracter, codigo])
        j += 1
    return lista

def Descomprimir(compressed, original):
    with open(original, 'w') as archD:
        cadena = ''
        tam = 1
        with open(compressed, 'rb') as archC:
            lista = CargarTabla(archC)
            c = archC.read(1)
            while (c):
                cadena += BinaryToString(c)
                while (tam < len(cadena)):
                    indice = BuscarCodigo(lista, cadena[0:tam])
                    if (indice != -1):
                        archD.write(lista[indice][0])
                        cadena = cadena[tam:]
                        tam = 1
                    else:
                        tam += 1
                
                c = archC.read(1)
        archC.close()
    archD.close()

#Main
sys.setrecursionlimit(100000)
#original = f'tp3_sample0.txt'
#compressed = f'tp3_sample0_compressed.bin'

original = f'super.txt'
compressed = f'super.bin'
descompressed = f'super_.txt'

#LeerArgumentos()
#Comprimir(original, compressed)
Descomprimir(compressed, descompressed)