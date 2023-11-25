import sys
import os
import math
import numpy as np
import time

BITE_SIZE = 8

def LeerArgumentos():
    args = sys.argv
    if (len(args) == 4):
        if (args[3] == "-c" and (os.path.exists(args[1])) or (args[3] == "-d" and os.path.exists(args[2]))):
            return True, args[1], args[2], args[3]
    return False, None, None, None

#Calculo de Datos
def LongitudMedia(lista):
    n = len(lista)
    l = 0
    for i in range(n):
        l = l + lista[i][1] * len(lista[i][2])
    return l

def CalcularEntropia(lista):
    n = len(lista)    
    entropia = 0.0
    for i in range(n):
        entropia = entropia + lista[i][1] * np.log2(1/lista[i][1])    
    return entropia

def MostrarDatos(lista, original, comprimido):
    tam_original = os.path.getsize(original)
    tam_comprimido = os.path.getsize(comprimido)
    tasa = tam_original / tam_comprimido

    long = LongitudMedia(lista)
    entropia = CalcularEntropia(lista)

    rendimiento = entropia / long
    redundancia = (long - entropia) / long

    print(f'Tasa de compresion {tasa:.4f}:1')
    print(f'\nPeso archivo original: {(tam_original/ 1024.):.4f} kb')
    print(f'Peso archivo comprimido: {(tam_comprimido/ 1024.):.4f} kb')
    print(f'\nRendimento: {rendimiento:.4f}')
    print(f'Redundancia: {redundancia:.4f}')

#Barra
def MostrarBarra(i, limit):
    p = i/limit
    i = int(30 * p)
    limit = int(limit/30)

    progress = f'{(100*p):3.0f}'    
    if (i >= 29):
        print(f'{progress} % [{"=" * 30}]', end='\r')
    else:        
        print(f'{progress} % [{"=" * i}>{"." * (29-i)}]', end='\r')

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
    while (indice < cant and lista[indice][2] != codigo):
        indice += 1

    if (indice >= cant):
        indice = -1

    return indice
def CalcularProbabilidades(lista, suma):
    cant = len(lista)
    i = 0
    while (i < cant): 
        lista[i][1] /= suma
        i += 1
    return lista

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

    return CalcularProbabilidades(lista, suma)

def RecorrerShannon_Fano(lista, a, b):
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

        lista = RecorrerShannon_Fano(lista, a, p)
        lista = RecorrerShannon_Fano(lista, f, b)
    else:
        if (a != b):
            lista[a][2] += '1'
            lista[b][2] += '0'
        else:
            lista[a][2] += '1'

    return lista
def Shannon_Fano(lista):
    lista = RecorrerShannon_Fano(lista, 0, len(lista) - 1)

    return lista

def RecorrerShannon_Huffman(arboles):    
    while (len(arboles) > 1):
        n1 = arboles[-1]
        n2 = arboles[-2]

        elem = [n1[0] + n2[0], n1, n2]

        arboles.pop(-1)
        arboles.pop(-1)

        i = len(arboles)
        while (i > 0 and elem[0] > arboles[i - 1][0]):
            i -= 1
        arboles.insert(i, elem)
    return arboles

def GenerarCodigo_Huffman(lista, nodo, cod):
    if (len(nodo) == 3):
        lista = GenerarCodigo_Huffman(lista, nodo[1], f'{cod}1')
        lista = GenerarCodigo_Huffman(lista, nodo[2], f'{cod}0')
    else:
        lista[nodo[1]][2] = cod
    return lista

def Huffman(lista):
    N = len(lista)
    arboles = []
    for i in range(N):
        arboles.append([lista[i][1], i])
    arboles = RecorrerShannon_Huffman(arboles)
    lista = GenerarCodigo_Huffman(lista, arboles[0], '')
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

def Comprimir(original, compressed):
    file_size = os.path.getsize(original)
    file_index = 1

    lista = LeerArchivo(original)

    #lista = Shannon_Fano(lista)
    lista = Huffman(lista)

    with open(compressed, 'wb') as archC:
        GuardarTabla(archC, lista)
        cadena = ''
        with open(original, 'r') as arch:            
            c = arch.read(1)
            while (c):

                indice = BuscarIndice(lista, c)
                cadena += lista[indice][2]

                while (len(cadena) > BITE_SIZE):
                    archC.write(StringToBinary(cadena[:BITE_SIZE]))
                    cadena = cadena[BITE_SIZE:]
                
                c = arch.read(1)
                MostrarBarra(file_index, file_size)
                file_index += 1

        if (len(cadena) > 0):
            archC.write(StringToBinary(cadena, right=True))
        
        arch.close()
    archC.close()
    print(end='\n')
    MostrarDatos(lista, original, compressed)

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

        lista.append([caracter, 0, codigo])
        j += 1
    return lista

def Descomprimir(compressed, original):
    file_size = os.path.getsize(compressed)
    file_index = None
    suma = 0
    with open(original, 'w') as archD:
        cadena = ''
        tam = 1
        with open(compressed, 'rb') as archC:
            lista = CargarTabla(archC)
            c = archC.read(1)
            file_index = archC.tell()
            while (c):

                MostrarBarra(file_index, file_size)
                file_index += 1

                cadena += BinaryToString(c)
                while (tam < len(cadena)):
                    indice = BuscarCodigo(lista, cadena[0:tam])
                    if (indice != -1):
                        archD.write(lista[indice][0])
                        cadena = cadena[tam:]                        
                        lista[indice][1] += 1
                        suma += 1
                        tam = 1
                    else:
                        tam += 1
                
                c = archC.read(1)
        archC.close()
    archD.close()

    print(end='\n')
    if (suma >= 0):
        lista = CalcularProbabilidades(lista, suma)
        MostrarDatos(lista, original, compressed)
    else:
        print("Error al descomprimir!")

#Main
sys.setrecursionlimit(100000)

argbool, url1, url2, flag = LeerArgumentos()

if (argbool):
    inicio_tiempo = time.time()
    if (flag == '-c'):
        Comprimir(url1, url2) #original, compressed
    else:
        Descomprimir(url2, url1) #compressed, descompressed
    fin_tiempo = time.time()
    print(f"\nTiempo transcurrido: {(fin_tiempo - inicio_tiempo):.4f} segundos")
else:
    print('\nError de argumentos')